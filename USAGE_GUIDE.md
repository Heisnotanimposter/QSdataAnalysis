# QSdataAnalysis - Usage Guide

## 🚀 Quick Start

### Option 1: Use the Startup Script (Recommended)
```bash
cd /Users/seungwonlee/QSdataAnalysis/QSdataAnalysis
./start_servers.sh
```

### Option 2: Manual Startup

#### Start API Server (FastAPI)
```bash
cd /Users/seungwonlee/QSdataAnalysis/QSdataAnalysis/univrank-app/api
python main.py
```
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

#### Start Web App (React)
```bash
cd /Users/seungwonlee/QSdataAnalysis/QSdataAnalysis/univrank-app
npm run dev
```
- **URL**: http://localhost:5173

## 📊 Available Endpoints

### API Server (http://localhost:8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rankings` | GET | Get all university rankings |
| `/university/{univ_id}` | GET | Get specific university details |
| `/stats` | GET | Get statistics about the dataset |
| `/docs` | GET | Interactive API documentation |
| `/health` | GET | Health check |

### Example API Calls

```bash
# Get all rankings
curl http://localhost:8000/rankings

# Get specific university
curl http://localhost:8000/university/U001

# Get statistics
curl http://localhost:8000/stats

# Health check
curl http://localhost:8000/health
```

## 🤖 Machine Learning Models

### Run Enhanced ML Model
```bash
cd "/Users/seungwonlee/QSdataAnalysis/QSdataAnalysis/university data"
python enhanced_ml.py
```

### Run Simple ML Model
```bash
cd "/Users/seungwonlee/QSdataAnalysis/QSdataAnalysis/university data"
python simple_ml.py
```

### Run TensorFlow Model (if dependencies available)
```bash
cd "/Users/seungwonlee/QSdataAnalysis/QSdataAnalysis/university data"
python main.py
```

## 📁 File Structure

```
QSdataAnalysis/
├── start_servers.sh              # Startup script
├── USAGE_GUIDE.md               # This file
├── README_FIXED.md              # Fixed issues documentation
├── world_university_rankings_2026.csv  # Main dataset
├── university data/             # ML models
│   ├── enhanced_ml.py          # Advanced Random Forest
│   ├── simple_ml.py            # Basic Linear Regression
│   ├── main.py                 # TensorFlow version
│   ├── requirements.txt        # Basic dependencies
│   └── requirements_enhanced.txt # Full dependencies
└── univrank-app/               # Web application
    ├── api/
    │   ├── main.py             # FastAPI server
    │   └── server.py          # Flask server (backup)
    ├── src/                   # React frontend
    └── package.json
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Permission Denied
```bash
# Make scripts executable
chmod +x start_servers.sh
chmod +x univrank-app/api/main.py
```

### Dependencies Missing
```bash
# Install ML dependencies
cd "university data"
pip install -r requirements_enhanced.txt

# Install API dependencies
cd univrank-app/api
pip install fastapi uvicorn pandas

# Install web app dependencies
cd univrank-app
npm install
```

### API Not Responding
1. Check if the API server is running: `curl http://localhost:8000/health`
2. Check logs for errors
3. Verify CSV file exists at the correct path
4. Try the Flask backup server: `python univrank-app/api/server.py`

### Web App Not Loading
1. Check if React dev server is running on port 5173
2. Check browser console for errors
3. Verify API server is accessible
4. Try clearing browser cache

## 📈 Model Performance

### Enhanced Model Results
- **Training R²**: 0.8726
- **Test R²**: 0.3211
- **Training MAE**: 1.1913
- **Test MAE**: 2.5565
- **Features**: 10 economic and institutional indicators

### Top Features
1. Nobel Laureates (31.89%)
2. Student Population (15.33%)
3. International Students % (12.29%)
4. University Age (10.14%)
5. Unemployment Rate (8.51%)

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| Web Application | http://localhost:5173 | Main university rankings interface |
| API Server | http://localhost:8000 | Backend API |
| API Documentation | http://localhost:8000/docs | Interactive API docs |
| Health Check | http://localhost:8000/health | Server status |

## 📊 Data Overview

- **Total Universities**: 59 in CSV, 57 processed
- **Countries**: 11 major countries with economic data
- **Ranking Systems**: QS, THE, ARWU
- **Features**: 10 economic and institutional indicators
- **Years**: 2025-2026 rankings

## 🔄 Data Flow

1. **CSV Data** → **API Server** → **Web App**
2. **Economic Data** → **ML Models** → **Predictions**
3. **Frontend** → **API Calls** → **Dynamic Rankings**

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Verify all dependencies are installed
3. Check server logs for error messages
4. Ensure ports 8000 and 5173 are available
5. Try restarting the servers using the startup script
