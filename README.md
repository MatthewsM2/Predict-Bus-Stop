# 🚌 Bus Stop Predictor

A web application for predicting bus stops from GPX track data.

---

## 🚀 Features

- Web-based GPX file upload  
- Automatic bus stop prediction using clustering algorithms  
- Interactive map visualization of predicted bus stops  
- Statistical analysis with confidence scores  
- Links to OpenStreetMap for each predicted stop  

---

## 🛠 Installation

1. Clone this repository  
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`  

---

## ⚙️ How It Works

1. **Data Collection**: Upload GPX files containing vehicle movement data  
2. **Preprocessing**: Extract coordinates, speed, and timestamps from GPX files  
3. **Stop Detection**: Identify points where speed is zero (vehicle stopped)  
4. **Clustering**: Group nearby stop points using DBSCAN algorithm  
5. **Analysis**: Calculate confidence scores based on recurring patterns  
6. **Visualization**: Display results on interactive maps and charts  

---

## 🧰 Technologies Used

- **Backend**: Python, Flask  
- **Data Processing**: Pandas, Scikit-learn, NumPy  
- **Frontend**: Leaflet.js, Chart.js, Bootstrap 5, HTML5, CSS3, JavaScript  

---

## 🔗 Links

- **Source Code Website**: [https://github.com/MatthewsM2/Predict-Bus-Stop](https://github.com/MatthewsM2/Predict-Bus-Stop)  
- **Live**:[https://github.com/MatthewsM2/Predict-Bus-Stop](https://github.com/MatthewsM2/Predict-Bus-Stop)
- **License**: GPL-3.0 license – see [LICENSE](https://github.com/MatthewsM2/Predict-Bus-Stop/blob/main/LICENSE) for details  
---
`#VibeCoding`