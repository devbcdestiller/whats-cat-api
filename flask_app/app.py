from flask import Flask, request, jsonify
from flask_cors import CORS
from classes import BREEDS
from PIL import Image
from io import BytesIO
import requests
import base64
import json


VERSION = 'v1'

# URI which points to the tensorflow-serving model
MODEL_URI = 'http://tf_serving:8501/v1/models/whatscat_model:predict'
app = Flask(__name__)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})


@app.route(f'/{VERSION}/predict', methods=['POST'])
def predict():
    input_img = request.files['img']
    accepted_img_format = ['image/jpeg', 'image/png']

    if input_img.content_type not in accepted_img_format:
        return jsonify(message='File format not supported. Use JPEG or PNG.'), 406

    img = Image.open(input_img)

    # encode image into base 64 since tf serving only accepts base 64 encoded images
    with BytesIO() as buffer:
        img.save(buffer, format='JPEG')
        b64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

    instance = [{"b64": b64_img}]
    data = json.dumps({"instances": instance})
    response = requests.post(MODEL_URI, data=data)
    result = json.loads(response.text)
    predictions = result['predictions'][0]
    res = dict(zip(predictions, BREEDS))
    sorted_data = sorted(res.items(), reverse=True)
    breeds = {k: v for k, v in enumerate(sorted_data)}

    return jsonify(message="Prediction Success", predictions=breeds)


@app.route('/')
def index():
    return 'Welcome! visit https://github.com/devbcdestiller/whats-cat-api to read the docs.'

# if __name__ == '__main__':
#     app.run(debug=True)
