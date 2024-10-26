from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import numpy as np

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your trained model
model = joblib.load('regressor.pkl')  # Ensure the path to the model is correct

@app.route('/')
def home():
    return "Welcome to the Insurance Cost Prediction API! Use the /predict endpoint to make predictions."

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.json
    
    # Extract input data in the specified order
    age = data.get('age')
    sex = 0 if data.get('sex') == 'male' else 1  # Encode gender as 0 for male, 1 for female
    bmi = data.get('bmi')
    children = data.get('children')
    smoker = 0 if data.get('smoker') == 'no' else 1  # Encode smoker as 0 for yes, 1 for no
    region = data.get('region')
    
    # Convert region to numerical value based on how it was encoded in your model
    region_dict = {'northwest': 3, 'northeast': 2, 'southwest': 1, 'southeast': 0}
    region_num = region_dict.get(region, -1)  # Default to -1 if region is not found

    # Check if the region is valid
    if region_num == -1:
        return jsonify({'error': 'Invalid region provided.'}), 400

    # Format the input data for model prediction
    input_data = np.array([[age, sex, bmi, children, smoker, region_num]])

    # Predict insurance cost using the loaded model
    predicted_cost = model.predict(input_data)[0]

    # Check if the predicted cost is less than 0, set to 0 if true
    if predicted_cost < 0:
        predicted_cost = 0

    # Return the prediction as a JSON response
    return jsonify({'predicted_cost': round(predicted_cost, 2)})

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development
