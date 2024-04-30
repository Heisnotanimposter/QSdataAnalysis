import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import datetime

# University scores for merging into economic data
university_scores = {
    'United States': 83.53,
    'United Kingdom': 84.24,
    'Australia': 83.18,
    'Canada': 83.83,
    'China': 79.68,  # Adjusted 'China (Mainland)' to 'China'
    'Switzerland': 86.85,
    'Singapore': 88.6,
    'France': 76.15,
    'Hong Kong': 73.64,
    'Japan': 80.3,
    'Germany': 76.25
}

# Merged data with university scores and economic factors
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

# Extract features and labels
features = np.array([[info['GDP_per_capita'], info['Unemployment_Rate']] for info in data.values()])
labels = np.array([info['University_Score'] for info in data.values()])

# Normalizing features
mean = features.mean(axis=0)
std = features.std(axis=0)
features = (features - mean) / std

# Model definition
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(2,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Setting up TensorBoard
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# Train the model
model.fit(features, labels, epochs=100, callbacks=[tensorboard_callback])

# Instructions to view TensorBoard
%load_ext tensorboard
%tensorboard --logdir logs/fit