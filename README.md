# Bus Stop Predictor

A web application for predicting bus stops from GPX track data.

## Features

- Web-based GPX file upload
- Automatic bus stop prediction using clustering algorithms
- Interactive map visualization of predicted bus stops
- Statistical analysis with confidence scores
- Links to OpenStreetMap for each predicted stop

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## How It Works

1. **Data Collection**: Upload GPX files containing vehicle movement data
2. **Preprocessing**: Extract coordinates, speed, and timestamps from GPX files
3. **Stop Detection**: Identify points where speed is zero (vehicle stopped)
4. **Clustering**: Group nearby stop points using DBSCAN algorithm
5. **Analysis**: Calculate confidence scores based on recurring patterns
6. **Visualization**: Display results on interactive maps and charts

## Technologies Used

- Python, Flask
- Pandas, Scikit-learn, NumPy
- Leaflet.js, Chart.js
- Bootstrap 5
- HTML5, CSS3, JavaScript