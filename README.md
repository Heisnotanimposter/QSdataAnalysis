# University Score and Economic Data Analysis

This project uses machine learning techniques to analyze the relationship between university scores and economic factors, such as GDP per capita and unemployment rate, across various countries. The project leverages TensorFlow and Keras for building and training the model, along with TensorBoard for visualization.

## Features
- **Data Integration**: Merges university scores with economic data for selected countries.
- **Machine Learning Model**: A neural network predicts university scores based on economic indicators.
- **Visualization**: TensorBoard integration for tracking training performance.

## Project Files
- **`main.py`**: Contains the main script for data processing, model definition, and training.
- **`data.json`**: (Optional) A JSON file for storing the economic and university score data.
- **`logs/`**: Directory containing TensorBoard logs for visualizing model performance.

## Data Overview
The project integrates the following data for each country:

| Country         | GDP per Capita | Unemployment Rate | University Score |
|-----------------|----------------|-------------------|------------------|
| United States   | 77,200         | 5.5%              | 83.53           |
| United Kingdom  | 45,000         | 4.1%              | 84.24           |
| Australia       | 55,000         | 5.2%              | 83.18           |
| Canada          | 46,000         | 5.7%              | 83.83           |
| China           | 10,052         | 5.3%              | 79.68           |
| Switzerland     | 83,000         | 4.4%              | 86.85           |
| Singapore       | 65,000         | 2.1%              | 88.60           |
| France          | 42,000         | 7.1%              | 76.15           |
| Hong Kong       | 49,000         | 3.3%              | 73.64           |
| Japan           | 40,000         | 2.4%              | 80.30           |
| Germany         | 43,361         | 6.0%              | 76.25           |

## Model Architecture
The neural network is a fully connected model with the following layers:
1. **Input Layer**: Accepts two features (GDP per capita and unemployment rate).
2. **Hidden Layers**:
   - Two dense layers with 64 units and ReLU activation.
3. **Output Layer**: A single dense layer predicting the university score.

## Installation
### Prerequisites
- Python 3.7+
- TensorFlow 2.x
- NumPy

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install required dependencies:
   ```bash
   pip install tensorflow numpy
   ```

## Running the Project
1. Run the script:
   ```bash
   python main.py
   ```
2. Start TensorBoard to visualize training progress:
   ```bash
   tensorboard --logdir logs/fit
   ```
3. Open TensorBoard in your browser to view performance metrics.

## Results
- The model predicts university scores based on economic factors with the goal of minimizing mean squared error.
- Training metrics (loss, accuracy) are visualized in TensorBoard.

## Customization
- **Add More Features**: Extend the `data` dictionary with additional economic or social indicators.
- **Adjust Model Parameters**: Modify the number of layers, units, or epochs to improve performance.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Acknowledgments
- TensorFlow documentation
- Publicly available economic and university score datasets

## Contact
For any questions or contributions, please reach out to the project maintainer.
