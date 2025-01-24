from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load models once at startup
with open('english.pkl', 'rb') as f:
    english_model = pickle.load(f)
with open('arabic.pkl', 'rb') as f:
    arabic_model = pickle.load(f)

# Define a constant API key for simplicity (use secure storage in production)
API_KEY = "c224864630499b96b9cef877fa8843dc30d739c27b57ee7a8b8e290059c09f5fa748b9a66bba505e386c3142efd9459d18ab1f591d32aaeb3b768f48096d7931d2b5c4e952595e8f670734a10475eea218fd17a3c39ac924e535444cbe4a842299481ab859a989f21af94ad91f88b417693b5369d1c13213387f8c651cfd4dc36e0bfb965cd153a40387173bc4f911ddf20ad5c71516c3864ca734b676cb21134d34a55e577aa1d7151377f2e81c5661e06100101e81181857f8f6f6289fdaf3e0a49ac6a6da6ad4c08bc9c83f09de65414db1f37ac4a65c2a4776f4a4cce9eb91e261ec8d8180b3efc76e0f2aa89e2dd329406667a31dceaa3f088b79b50d47"

# Middleware function for API key validation
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')  # Expecting "Api-Key your-secure-api-key"
        if not api_key or not api_key.startswith("Api-Key "):
            return jsonify({'error': 'Unauthorized: Missing or invalid API key'}), 401
        
        provided_key = api_key.split(" ")[1]  # Extract the actual key
        if provided_key != API_KEY:
            return jsonify({'error': 'Unauthorized: Invalid API key'}), 401
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/predict/english', methods=['POST'])
@require_api_key  # Apply the API key validation
def predict_model2():
    review = request.args.get('review')
    if not review:
        return jsonify({'error': 'Missing review parameter'}), 400

    x = english_model(review) 
    y = x[0]["label"].lower() 
    print(y)
    return jsonify({'prediction': y})

@app.route('/predict/arabic', methods=['POST'])
@require_api_key  # Apply the API key
def predict_model1():
    review = request.args.get('review')
    if not review:
        return jsonify({'error': 'Missing review parameter'}), 400

    x = arabic_model(review) 
    y = x[0]["label"].lower() 
    print(y)
    return jsonify({'prediction': y})

if __name__ == '__main__':
    app.run()
