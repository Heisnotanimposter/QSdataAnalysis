import numpy as np
import pandas as pd

# Simple ML implementation without TensorFlow to avoid dependency issues
class SimpleLinearRegression:
    def __init__(self):
        self.weights = None
        self.bias = None
        
    def fit(self, X, y, learning_rate=0.01, epochs=1000):
        # Initialize parameters
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # Gradient descent
        for epoch in range(epochs):
            # Forward pass
            y_predicted = np.dot(X, self.weights) + self.bias
            
            # Calculate gradients
            dw = (1/n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1/n_samples) * np.sum(y_predicted - y)
            
            # Update parameters
            self.weights -= learning_rate * dw
            self.bias -= learning_rate * db
            
            if epoch % 100 == 0:
                loss = np.mean((y_predicted - y) ** 2)
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
    
    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
    
    def score(self, X, y):
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot)

# Load university data
def load_university_data():
    try:
        df = pd.read_csv('../world_university_rankings_2026.csv')
        return df
    except FileNotFoundError:
        print("CSV file not found. Using fallback data.")
        return None

# Economic data for countries
economic_data = {
    'USA': {'GDP_per_capita': 77200, 'Unemployment_Rate': 5.5},
    'UK': {'GDP_per_capita': 45000, 'Unemployment_Rate': 4.1},
    'Australia': {'GDP_per_capita': 55000, 'Unemployment_Rate': 5.2},
    'Canada': {'GDP_per_capita': 46000, 'Unemployment_Rate': 5.7},
    'China': {'GDP_per_capita': 10052, 'Unemployment_Rate': 5.3},
    'Switzerland': {'GDP_per_capita': 83000, 'Unemployment_Rate': 4.4},
    'Singapore': {'GDP_per_capita': 65000, 'Unemployment_Rate': 2.1},
    'France': {'GDP_per_capita': 42000, 'Unemployment_Rate': 7.1},
    'Hong Kong': {'GDP_per_capita': 49000, 'Unemployment_Rate': 3.3},
    'Japan': {'GDP_per_capita': 40000, 'Unemployment_Rate': 2.4},
    'Germany': {'GDP_per_capita': 43361, 'Unemployment_Rate': 6.0}
}

# Prepare dataset
def prepare_dataset():
    df = load_university_data()
    if df is None:
        # Fallback to original hardcoded data
        data = {
            'United States': {'GDP_per_capita': 77200, 'Unemployment_Rate': 5.5, 'University_Score': 83.53},
            'United Kingdom': {'GDP_per_capita': 45000, 'Unemployment_Rate': 4.1, 'University_Score': 84.24},
            'Australia': {'GDP_per_capita': 55000, 'Unemployment_Rate': 5.2, 'University_Score': 83.18},
            'Canada': {'GDP_per_capita': 46000, 'Unemployment_Rate': 5.7, 'University_Score': 83.83},
            'China': {'GDP_per_capita': 10052, 'Unemployment_Rate': 5.3, 'University_Score': 79.68},
            'Switzerland': {'GDP_per_capita': 83000, 'Unemployment_Rate': 4.4, 'University_Score': 86.85},
            'Singapore': {'GDP_per_capita': 65000, 'Unemployment_Rate': 2.1, 'University_Score': 88.6},
            'France': {'GDP_per_capita': 42000, 'Unemployment_Rate': 7.1, 'University_Score': 76.15},
            'Hong Kong': {'GDP_per_capita': 49000, 'Unemployment_Rate': 3.3, 'University_Score': 73.64},
            'Japan': {'GDP_per_capita': 40000, 'Unemployment_Rate': 2.4, 'University_Score': 80.3},
            'Germany': {'GDP_per_capita': 43361, 'Unemployment_Rate': 6.0, 'University_Score': 76.25}
        }
        return data
    
    # Process CSV data
    processed_data = {}
    for _, row in df.iterrows():
        country = row['country']
        if country in economic_data:
            # Use QS score as the target variable
            university_score = row['qs_score'] if pd.notna(row['qs_score']) else 75.0  # fallback score
            
            if country not in processed_data:
                processed_data[country] = {
                    'GDP_per_capita': economic_data[country]['GDP_per_capita'],
                    'Unemployment_Rate': economic_data[country]['Unemployment_Rate'],
                    'University_Scores': []
                }
            processed_data[country]['University_Scores'].append(university_score)
    
    # Calculate average university score per country
    final_data = {}
    for country, data in processed_data.items():
        avg_score = np.mean(data['University_Scores'])
        final_data[country] = {
            'GDP_per_capita': data['GDP_per_capita'],
            'Unemployment_Rate': data['Unemployment_Rate'],
            'University_Score': avg_score
        }
    
    return final_data

# Main execution
if __name__ == "__main__":
    print("Loading and preparing dataset...")
    data = prepare_dataset()
    print(f"Dataset prepared with {len(data)} countries")
    
    # Extract features and labels
    features = np.array([[info['GDP_per_capita'], info['Unemployment_Rate']] for info in data.values()])
    labels = np.array([info['University_Score'] for info in data.values()])
    
    print(f"Features shape: {features.shape}")
    print(f"Labels shape: {labels.shape}")
    
    # Normalize features
    mean = features.mean(axis=0)
    std = features.std(axis=0)
    features_normalized = (features - mean) / std
    
    print(f"Feature normalization - Mean: {mean}, Std: {std}")
    
    # Split data
    split_idx = int(len(features_normalized) * 0.8)
    X_train, X_val = features_normalized[:split_idx], features_normalized[split_idx:]
    y_train, y_val = labels[:split_idx], labels[split_idx:]
    
    # Train model
    print("\nTraining simple linear regression model...")
    model = SimpleLinearRegression()
    model.fit(X_train, y_train, learning_rate=0.01, epochs=1000)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    val_score = model.score(X_val, y_val)
    
    print(f"\nModel Performance:")
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Validation R² Score: {val_score:.4f}")
    
    # Make predictions
    predictions = model.predict(features_normalized)
    
    print("\nPredictions vs Actual:")
    print("-" * 50)
    for i, (country, actual) in enumerate(data.items()):
        predicted = predictions[i]
        print(f"{country:15} | Predicted: {predicted:6.2f} | Actual: {actual['University_Score']:6.2f} | Diff: {abs(predicted - actual['University_Score']):5.2f}")
    
    # Save model parameters
    np.savez('model_params.npz', weights=model.weights, bias=model.bias, mean=mean, std=std)
    print("\nModel parameters saved to model_params.npz")
    
    # Feature importance (weights)
    print(f"\nFeature Importance:")
    print(f"GDP per Capita Weight: {model.weights[0]:.6f}")
    print(f"Unemployment Rate Weight: {model.weights[1]:.6f}")
    print(f"Bias: {model.bias:.6f}")
