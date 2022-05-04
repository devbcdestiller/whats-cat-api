from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from classes import BREEDS
from PIL import Image
from io import BytesIO
from pymemcache.client.base import Client
import ast
import requests
import base64
import json
import os

VERSION = 'v1'
app = Flask(__name__)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

# Setup Memcache global variables
MEMCACHE_CLIENT = Client(('memcache', 11211), no_delay=True)
MEMCACHE_EXPIRE = 60 # cached object will expire in 60 seconds

# URI which points to the tensorflow-serving model
MODEL_URI = 'http://tf_serving:8501/v1/models/whatscat_model:predict'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route(f'/{VERSION}/predict', methods=['POST'])
def predict():
    input_img = request.files['img']
    accepted_img_format = ['image/jpeg', 'image/png']

    if input_img.content_type not in accepted_img_format:
        return jsonify(message='File format not supported. Use JPEG or PNG.'), 406

    with Image.open(input_img) as img:

        # tensorflow serving container becomes buggy when image resolution is greater that 1080p
        if (img.width * img.height) > 2073600:
            if img.height > img.width:
                img = img.resize((1080, 1920))
            else:
                img = img.resize((1920, 1080))

        # encode image into base 64 since tf serving only accepts base 64 encoded images
        with BytesIO() as buffer:
            img.save(buffer, format='JPEG', optimize=True, quality=60)
            b64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

        memcache_key = b64_img[-32:-1]

        if MEMCACHE_CLIENT.get(memcache_key) is not None:
            cached_result = MEMCACHE_CLIENT.get(memcache_key)
            cached_result = ast.literal_eval(cached_result.decode('utf-8'))
            return jsonify(image=input_img.filename, message="Cached Prediction", predictions=cached_result, memkey=memcache_key)

    instance = [{"b64": b64_img}]
    data = json.dumps({"instances": instance})
    response = requests.post(MODEL_URI, data=data)
    result = json.loads(response.text)
    predictions = result['predictions'][0]
    res = dict(zip(predictions, BREEDS))
    sorted_data = sorted(res.items(), reverse=True)
    breeds = {k: v for k, v in enumerate(sorted_data)}

    MEMCACHE_CLIENT.add(memcache_key, breeds, expire=MEMCACHE_EXPIRE, noreply=False)

    return jsonify(message="Prediction Success", predictions=breeds)


@app.route('/')
def index():
    return 'Welcome! visit https://github.com/devbcdestiller/whats-cat-api to read the docs.'


# if __name__ == '__main__':
#     app.run(debug=True)
