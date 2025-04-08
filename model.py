import os
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from sklearn.cluster import DBSCAN
from collections import defaultdict
import folium
import matplotlib.pyplot as plt
import plotly.express as px

# Step 1: Parse GPX files and preprocess data
def parse_gpx(file_path):
    """
    Parse a GPX file and extract latitude, longitude, speed, and timestamp.
    """
    data = []
    with open(file_path, 'r') as file:
        lat, lon, speed, timestamp = None, None, None, None
        for line in file:
            if '<trkpt' in line:
                lat = float(line.split('lat="')[1].split('"')[0])
                lon = float(line.split('lon="')[1].split('"')[0])
            elif '<speed>' in line:
                speed = float(line.split('<speed>')[1].split('</speed>')[0])
            elif '<time>' in line:
                timestamp = line.split('<time>')[1].split('</time>')[0]
            
            # If all values are available, append to data
            if lat is not None and lon is not None and speed is not None and timestamp is not None:
                data.append([lat, lon, speed, timestamp, os.path.basename(file_path)])  # Include file name
                lat, lon, speed, timestamp = None, None, None, None  # Reset for next track point
    return pd.DataFrame(data, columns=['latitude', 'longitude', 'speed', 'timestamp', 'file_name'])

# Step 2: Preprocess and calculate stop duration
def preprocess_data(df):
    """
    Calculate stop duration and filter zero-speed points.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # Calculate time difference between consecutive points
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    
    # Identify stops (where speed is 0)
    df['is_stop'] = (df['speed'] == 0).astype(int)
    
    # Calculate stop duration
    df['stop_duration'] = df.groupby((df['is_stop'] != df['is_stop'].shift()).cumsum())['time_diff'].cumsum()
    
    # Filter only stop points
    stop_df = df[df['is_stop'] == 1]
    return stop_df

# Step 3: Cluster stop points using DBSCAN
def cluster_stops(stop_df, eps=0.001, min_samples=2):
    """
    Cluster stop points using DBSCAN to identify frequent bus stops.
    """
    coords = stop_df[['latitude', 'longitude']].values
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    stop_df['cluster'] = db.labels_
    return stop_df

# Step 4: Analyze clusters and generate bus stop predictions
def analyze_clusters(stop_df):
    """
    Analyze clusters to generate a list of potential bus stops.
    """
    cluster_stats = defaultdict(lambda: {'files': set(), 'points': []})  # Use a set to store unique file names
    
    for _, row in stop_df.iterrows():
        cluster_id = row['cluster']
        if cluster_id != -1:  # Ignore noise points
            cluster_stats[cluster_id]['files'].add(row['file_name'])  # Add file name to the set
            cluster_stats[cluster_id]['points'].append((row['latitude'], row['longitude']))
    
    # Calculate mean coordinates for each cluster
    bus_stops = []
    for cluster_id, stats in cluster_stats.items():
        mean_lat = np.mean([p[0] for p in stats['points']])
        mean_lon = np.mean([p[1] for p in stats['points']])
        bus_stops.append({
            'latitude': mean_lat,
            'longitude': mean_lon,
            'supporting_files': len(stats['files']),  # Count unique files
            'confidence': len(stats['files']) / len(stop_df['file_name'].unique())  # Confidence based on unique files
        })
    
    return pd.DataFrame(bus_stops)

# Step 5: Main function to process all GPX files in a folder
def process_gpx_files_in_folder(folder_path):
    """
    Process all GPX files in a folder and generate bus stop predictions.
    """
    all_stops = pd.DataFrame()
    
    # Get all GPX files in the folder
    gpx_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.gpx')]
    
    for file_path in gpx_files:
        try:
            df = parse_gpx(file_path)
            stop_df = preprocess_data(df)
            all_stops = pd.concat([all_stops, stop_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    # Cluster stops from all files
    clustered_stops = cluster_stops(all_stops)
    bus_stops = analyze_clusters(clustered_stops)
    
    return bus_stops