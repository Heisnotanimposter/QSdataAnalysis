# QSdataAnalysis - Fixed and Enhanced Version

## Issues Fixed

### 1. ✅ Lack of University Data
- **Problem**: ML model used only 11 hardcoded countries
- **Solution**: Integrated comprehensive CSV dataset with 59 universities
- **Result**: Now processes 46 universities across 11 countries with real ranking data

### 2. ✅ Functional Errors
- **Problem**: `test1.py` had syntax error with Jupyter magic commands
- **Solution**: Created multiple working implementations:
  - `simple_ml.py` - Basic linear regression without dependencies
  - `enhanced_ml.py` - Advanced Random Forest with 10 features
  - `main.py` - TensorFlow version (when dependencies allow)

### 3. ✅ Lack of Data Integration
- **Problem**: Web app used static JSON, ML model used hardcoded data
- **Solution**: 
  - Created Flask API server (`api/server.py`) serving CSV data
  - Enhanced ML model with 10 economic and institutional features
  - Added comprehensive feature importance analysis

## New Features Added

### Enhanced ML Model
- **10 Features**: GDP per capita, unemployment, R&D spending, education expenditure, internet penetration, innovation index, university age, student population, international students, Nobel laureates
- **Advanced Algorithms**: Random Forest with cross-validation
- **Performance Metrics**: R², MAE, MSE with detailed analysis
- **Visualizations**: Feature importance plots, prediction analysis

### Web App Improvements
- **Live API Server**: Flask backend serving real CSV data
- **Fallback System**: Graceful degradation to static JSON
- **Error Handling**: Comprehensive error management
- **Data Structure**: Unified format between CSV and frontend

### Data Processing
- **46 Universities**: Processed from 59 in original CSV
- **11 Countries**: USA, UK, Australia, Canada, China, Switzerland, Singapore, France, Hong Kong, Japan, Germany
- **Multiple Rankings**: QS, THE, ARWU integration
- **Economic Context**: R&D spending, education expenditure, innovation metrics

## Performance Results

### Enhanced Model Performance
- **Training R²**: 0.8726
- **Test R²**: 0.3211
- **Training MAE**: 1.1913
- **Test MAE**: 2.5565

### Feature Importance (Top 5)
1. Nobel Laureates (31.89%)
2. Student Population (15.33%)
3. International Students % (12.29%)
4. University Age (10.14%)
5. Unemployment Rate (8.51%)

## File Structure

```
QSdataAnalysis/
├── university data/
│   ├── simple_ml.py              # Basic linear regression
│   ├── enhanced_ml.py            # Advanced Random Forest
│   ├── main.py                   # TensorFlow version
│   ├── requirements.txt          # Basic dependencies
│   ├── requirements_enhanced.txt # Full dependencies
│   └── model_params.npz          # Trained model parameters
├── univrank-app/
│   ├── api/
│   │   └── server.py             # Flask API server
│   ├── requirements.txt          # API dependencies
│   └── src/                      # React frontend (working)
├── world_university_rankings_2026.csv  # Main dataset
└── README_FIXED.md               # This file
```

## Running the Applications

### 1. ML Models
```bash
# Basic model (no extra dependencies)
cd "university data"
python simple_ml.py

# Enhanced model (requires scikit-learn, matplotlib, seaborn)
pip install -r requirements_enhanced.txt
python enhanced_ml.py
```

### 2. Web Application
```bash
# Start API server
cd univrank-app/api
python server.py

# Start React app (new terminal)
cd univrank-app
npm run dev

# Access at http://localhost:5173
```

## Key Improvements

1. **Data Integration**: Full CSV integration with fallback systems
2. **Model Performance**: Multiple algorithms with comprehensive evaluation
3. **Feature Engineering**: 10 relevant features vs original 2
4. **Error Handling**: Robust error management and graceful degradation
5. **Visualization**: Feature importance and prediction analysis
6. **Documentation**: Clear file structure and usage instructions

## Remaining Limitations

1. **Dataset Size**: Still limited to 46 universities due to economic data availability
2. **Model Overfitting**: High training R² vs test R² indicates some overfitting
3. **API Dependencies**: Flask server needs to be running separately
4. **Browser Compatibility**: Some visualization features may need modern browsers

## Future Enhancements

1. **More Economic Data**: Add more countries with comprehensive economic indicators
2. **Advanced Models**: Try gradient boosting, neural networks
3. **Real-time Data**: API integration for live economic data
4. **Interactive Dashboard**: Enhanced web interface with ML predictions
5. **Cross-validation**: More robust model validation techniques
