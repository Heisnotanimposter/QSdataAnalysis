import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import json

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class EnhancedUniversityPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_names = []
        self.scaler_mean = None
        self.scaler_std = None
        
    def load_and_process_data(self):
        """Load university data and create enhanced features"""
        try:
            df = pd.read_csv('../world_university_rankings_2026.csv')
            print(f"Loaded {len(df)} universities from CSV")
        except FileNotFoundError:
            print("CSV file not found. Using fallback data.")
            return None, None, None
        
        # Extended economic data with more features
        economic_data = {
            'USA': {
                'GDP_per_capita': 77200, 'Unemployment_Rate': 5.5, 'R&D_Spending_GDP': 3.45,
                'Education_Expenditure_GDP': 6.2, 'Internet_Penetration': 92.1, 'Innovation_Index': 1.8
            },
            'UK': {
                'GDP_per_capita': 45000, 'Unemployment_Rate': 4.1, 'R&D_Spending_GDP': 1.74,
                'Education_Expenditure_GDP': 5.4, 'Internet_Penetration': 95.0, 'Innovation_Index': 1.5
            },
            'Australia': {
                'GDP_per_capita': 55000, 'Unemployment_Rate': 5.2, 'R&D_Spending_GDP': 1.79,
                'Education_Expenditure_GDP': 5.9, 'Internet_Penetration': 86.5, 'Innovation_Index': 1.4
            },
            'Canada': {
                'GDP_per_capita': 46000, 'Unemployment_Rate': 5.7, 'R&D_Spending_GDP': 1.71,
                'Education_Expenditure_GDP': 5.3, 'Internet_Penetration': 94.0, 'Innovation_Index': 1.3
            },
            'China': {
                'GDP_per_capita': 10052, 'Unemployment_Rate': 5.3, 'R&D_Spending_GDP': 2.40,
                'Education_Expenditure_GDP': 3.9, 'Internet_Penetration': 70.0, 'Innovation_Index': 1.2
            },
            'Switzerland': {
                'GDP_per_capita': 83000, 'Unemployment_Rate': 4.4, 'R&D_Spending_GDP': 3.14,
                'Education_Expenditure_GDP': 5.6, 'Internet_Penetration': 96.0, 'Innovation_Index': 1.7
            },
            'Singapore': {
                'GDP_per_capita': 65000, 'Unemployment_Rate': 2.1, 'R&D_Spending_GDP': 2.16,
                'Education_Expenditure_GDP': 2.9, 'Internet_Penetration': 88.0, 'Innovation_Index': 1.6
            },
            'France': {
                'GDP_per_capita': 42000, 'Unemployment_Rate': 7.1, 'R&D_Spending_GDP': 2.22,
                'Education_Expenditure_GDP': 5.5, 'Internet_Penetration': 85.0, 'Innovation_Index': 1.1
            },
            'Hong Kong': {
                'GDP_per_capita': 49000, 'Unemployment_Rate': 3.3, 'R&D_Spending_GDP': 0.86,
                'Education_Expenditure_GDP': 3.8, 'Internet_Penetration': 92.0, 'Innovation_Index': 1.4
            },
            'Japan': {
                'GDP_per_capita': 40000, 'Unemployment_Rate': 2.4, 'R&D_Spending_GDP': 3.26,
                'Education_Expenditure_GDP': 4.0, 'Internet_Penetration': 91.0, 'Innovation_Index': 1.2
            },
            'Germany': {
                'GDP_per_capita': 43361, 'Unemployment_Rate': 6.0, 'R&D_Spending_GDP': 3.13,
                'Education_Expenditure_GDP': 4.7, 'Internet_Penetration': 89.0, 'Innovation_Index': 1.3
            }
        }
        
        # Process data by country
        processed_data = []
        for _, row in df.iterrows():
            country = row['country']
            if country in economic_data:
                econ = economic_data[country]
                
                # Create feature vector
                features = {
                    'GDP_per_capita': econ['GDP_per_capita'],
                    'Unemployment_Rate': econ['Unemployment_Rate'],
                    'R&D_Spending_GDP': econ['R&D_Spending_GDP'],
                    'Education_Expenditure_GDP': econ['Education_Expenditure_GDP'],
                    'Internet_Penetration': econ['Internet_Penetration'],
                    'Innovation_Index': econ['Innovation_Index'],
                    'University_Age': 2026 - row['founded'] if pd.notna(row['founded']) else 100,
                    'Student_Population': row['total_students'] if pd.notna(row['total_students']) else 10000,
                    'International_Students_Pct': row['intl_students_pct'] if pd.notna(row['intl_students_pct']) else 10,
                    'Nobel_Laureates': row['nobel_laureates'] if pd.notna(row['nobel_laureates']) else 0
                }
                
                # Target: Use QS score as primary, fallback to THE or ARWU
                target = None
                if pd.notna(row['qs_score']):
                    target = row['qs_score']
                elif pd.notna(row['the_score']):
                    target = row['the_score']
                elif pd.notna(row['arwu_score']):
                    target = row['arwu_score']
                else:
                    target = 75.0  # fallback
                
                processed_data.append({
                    'university': row['university'],
                    'country': country,
                    'features': features,
                    'target': target
                })
        
        return processed_data, economic_data, df
    
    def prepare_features_and_targets(self, processed_data):
        """Convert processed data to feature matrix and target vector"""
        if not processed_data:
            return None, None, None
        
        # Extract feature names
        self.feature_names = list(processed_data[0]['features'].keys())
        
        # Create feature matrix
        X = np.array([list(item['features'].values()) for item in processed_data])
        y = np.array([item['target'] for item in processed_data])
        
        # Normalize features
        self.scaler_mean = X.mean(axis=0)
        self.scaler_std = X.std(axis=0)
        X_normalized = (X - self.scaler_mean) / self.scaler_std
        
        return X_normalized, y, processed_data
    
    def train_and_evaluate(self, X, y):
        """Train model and evaluate performance"""
        if X is None:
            return None
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train)
        
        # Predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Metrics
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        
        print(f"\nModel Performance:")
        print(f"Training R²: {train_r2:.4f}")
        print(f"Test R²: {test_r2:.4f}")
        print(f"Training MAE: {train_mae:.4f}")
        print(f"Test MAE: {test_mae:.4f}")
        print(f"Training MSE: {train_mse:.4f}")
        print(f"Test MSE: {test_mse:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5, scoring='r2')
        print(f"Cross-validation R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return {
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_mse': train_mse,
            'test_mse': test_mse,
            'cv_scores': cv_scores.tolist()
        }
    
    def analyze_feature_importance(self):
        """Analyze and visualize feature importance"""
        if not hasattr(self.model, 'feature_importances_'):
            return None
        
        importance = self.model.feature_importances_
        feature_importance = list(zip(self.feature_names, importance))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        print("\nFeature Importance:")
        for feature, imp in feature_importance:
            print(f"{feature:25}: {imp:.4f}")
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        features, importances = zip(*feature_importance)
        plt.barh(features, importances)
        plt.xlabel('Importance')
        plt.title('Feature Importance for University Score Prediction')
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return feature_importance
    
    def create_predictions_analysis(self, X, y, processed_data):
        """Create detailed predictions analysis"""
        predictions = self.model.predict(X)
        
        # Create analysis dataframe
        analysis_data = []
        for i, item in enumerate(processed_data):
            analysis_data.append({
                'university': item['university'],
                'country': item['country'],
                'actual': y[i],
                'predicted': predictions[i],
                'error': abs(y[i] - predictions[i]),
                'percent_error': abs(y[i] - predictions[i]) / y[i] * 100
            })
        
        df_analysis = pd.DataFrame(analysis_data)
        df_analysis = df_analysis.sort_values('error')
        
        print("\nTop 10 Most Accurate Predictions:")
        print(df_analysis.head(10)[['university', 'country', 'actual', 'predicted', 'error']].to_string(index=False))
        
        print("\nTop 10 Least Accurate Predictions:")
        print(df_analysis.tail(10)[['university', 'country', 'actual', 'predicted', 'error']].to_string(index=False))
        
        # Save detailed results
        df_analysis.to_csv('predictions_analysis.csv', index=False)
        
        return df_analysis
    
    def save_model(self):
        """Save model and preprocessing parameters"""
        import joblib
        joblib.dump({
            'model': self.model,
            'feature_names': self.feature_names,
            'scaler_mean': self.scaler_mean,
            'scaler_std': self.scaler_std
        }, 'enhanced_university_model.joblib')
        print("Model saved to enhanced_university_model.joblib")

def main():
    print("=== Enhanced University Score Prediction System ===\n")
    
    # Initialize predictor
    predictor = EnhancedUniversityPredictor()
    
    # Load and process data
    processed_data, economic_data, raw_df = predictor.load_and_process_data()
    
    if processed_data is None:
        print("Failed to load data. Exiting.")
        return
    
    print(f"Processed {len(processed_data)} universities")
    
    # Prepare features
    X, y, processed_data = predictor.prepare_features_and_targets(processed_data)
    
    if X is None:
        print("Failed to prepare features. Exiting.")
        return
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Features: {predictor.feature_names}")
    
    # Train and evaluate
    metrics = predictor.train_and_evaluate(X, y)
    
    # Feature importance
    feature_importance = predictor.analyze_feature_importance()
    
    # Predictions analysis
    analysis_df = predictor.create_predictions_analysis(X, y, processed_data)
    
    # Save model
    predictor.save_model()
    
    # Save metrics
    with open('enhanced_model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("\n=== Analysis Complete ===")
    print("Files created:")
    print("- enhanced_university_model.joblib (trained model)")
    print("- enhanced_model_metrics.json (performance metrics)")
    print("- predictions_analysis.csv (detailed predictions)")
    print("- feature_importance.png (feature importance visualization)")

if __name__ == "__main__":
    main()
