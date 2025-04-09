from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from model import parse_gpx, preprocess_data, cluster_stops, analyze_clusters
import pandas as pd
import uuid

load_dotenv()
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'gpx'}

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    session_id = str(uuid.uuid4())
    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_folder, exist_ok=True)
    
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(session_folder, filename)
            file.save(file_path)
            uploaded_files.append(file_path)
    
    # Process the uploaded files
    if uploaded_files:
        all_stops = pd.DataFrame()
        for file_path in uploaded_files:
            try:
                df = parse_gpx(file_path)
                stop_df = preprocess_data(df)
                all_stops = pd.concat([all_stops, stop_df], ignore_index=True)
            except Exception as e:
                flash(f"Error processing file {os.path.basename(file_path)}: {e}")
        
        # Only proceed if we have data
        if not all_stops.empty:
            # Cluster stops from all files
            clustered_stops = cluster_stops(all_stops)
            bus_stops = analyze_clusters(clustered_stops)
            
            # Generate OSM links
            bus_stops['osm_link'] = bus_stops.apply(
                lambda row: f"https://www.openstreetmap.org/?mlat={row['latitude']}&mlon={row['longitude']}&zoom=17",
                axis=1
            )
            
            # Store results in session
            session['bus_stops'] = bus_stops.to_dict(orient='records')
            session['map_center'] = [bus_stops['latitude'].mean(), bus_stops['longitude'].mean()]
            
            return redirect(url_for('results'))
    
    flash('No valid GPX files were processed')
    return redirect(url_for('index'))

@app.route('/results')
def results():
    if 'bus_stops' not in session:
        flash('No analysis results available. Please upload GPX files first.')
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                           bus_stops=session['bus_stops'],
                           map_center=session['map_center'])

@app.route('/api/bus_stops')
def api_bus_stops():
    if 'bus_stops' not in session:
        return jsonify({'error': 'No data available'})
    
    return jsonify({
        'bus_stops': session['bus_stops'],
        'map_center': session['map_center']
    })

if __name__ == '__main__':
    app.run(debug=True)
