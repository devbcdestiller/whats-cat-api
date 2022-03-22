from flask import Flask, request, jsonify
from PIL import Image
from package.image_processing import ImageProcessing
from package.model_processing import ModelProcessing

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    input_img = request.files['img']
    accepted_img_format = ['image/jpeg', 'image/png']
    
    if input_img.content_type not in accepted_img_format:
        return jsonify(message='File format not supported. Use JPEG or PNG.'), 406

    img = Image.open(input_img)
    result = process_input(img)

    return jsonify(result)


def process_input(input_img):
    model_path = "package/models/cnnv2.h5"
    img = ImageProcessing(input_img)
    mp = ModelProcessing(img.image_to_array(), model_path)
    return mp.get_prediction()


if __name__ == '__main__':
    app.run()