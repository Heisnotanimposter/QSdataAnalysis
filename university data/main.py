import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd
import datetime
import json

# Load comprehensive university data from CSV
def load_university_data():
    try:
        df = pd.read_csv('../world_university_rankings_2026.csv')
        return df
    except FileNotFoundError:
        print("CSV file not found. Using fallback data.")
        return None

# Economic data for countries (can be expanded)
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

# Prepare comprehensive dataset
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

# Prepare dataset
data = prepare_dataset()
print(f"Dataset prepared with {len(data)} countries")

# Extract features and labels
features = np.array([[info['GDP_per_capita'], info['Unemployment_Rate']] for info in data.values()])
labels = np.array([info['University_Score'] for info in data.values()])

print(f"Features shape: {features.shape}")
print(f"Labels shape: {labels.shape}")

# Normalizing features
mean = features.mean(axis=0)
std = features.std(axis=0)
features_normalized = (features - mean) / std

# Enhanced model architecture
model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(2,)),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

# Compile the model with additional metrics
model.compile(
    optimizer='adam', 
    loss='mean_squared_error',
    metrics=['mae', 'mse']
)

# Print model summary
model.summary()

# Setting up TensorBoard
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=log_dir, 
    histogram_freq=1,
    write_graph=True,
    write_images=True
)

# Add early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True
)

# Split data for training and validation (simple split since dataset is small)
split_idx = int(len(features_normalized) * 0.8)
X_train, X_val = features_normalized[:split_idx], features_normalized[split_idx:]
y_train, y_val = labels[:split_idx], labels[split_idx:]

# Train the model
print("Training model...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=200,
    batch_size=4,
    callbacks=[tensorboard_callback, early_stopping],
    verbose=1
)

# Evaluate the model
print("\nEvaluating model...")
loss, mae, mse = model.evaluate(X_val, y_val, verbose=0)
print(f"Validation Loss: {loss:.4f}")
print(f"Validation MAE: {mae:.4f}")
print(f"Validation MSE: {mse:.4f}")

# Make predictions
predictions = model.predict(features_normalized)
print("\nPredictions vs Actual:")
for i, (country, actual) in enumerate(data.items()):
    predicted = predictions[i][0]
    print(f"{country}: Predicted={predicted:.2f}, Actual={actual['University_Score']:.2f}")

# Save the model and normalization parameters
model.save('university_economic_model.h5')
np.savez('normalization_params.npz', mean=mean, std=std)

print(f"\nModel saved successfully!")
print(f"To view TensorBoard, run: tensorboard --logdir {log_dir}")

# Save training history
with open('training_history.json', 'w') as f:
    json.dump(history.history, f, indent=2)

print("Training history saved to training_history.json")
