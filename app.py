from flask import Flask, request, jsonify
import joblib

# Load the pre-trained model
model = joblib.load('irisclf')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Ensure that the request is JSON and it contains the expected data
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    try:
        # Extract the features from the JSON object
        features = data['features']
        if len(features) != 4:
            raise ValueError("Incorrect number of features")

        feature1, feature2, feature3, feature4 = map(float, features)
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input data: {str(e)}"}), 400

    # Make predictions using the loaded model
    prediction = model.predict([[feature1, feature2, feature3, feature4]])

    # Return the prediction as JSON
    return jsonify({"prediction": int(prediction[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # Set debug=False in a production environment.
