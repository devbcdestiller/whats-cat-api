import tensorflow as tf
from package.models.predictions import BREEDS

class ModelProcessing():
    def __init__(self, input_img, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.input_img = input_img

    def get_prediction(self, top=3):
        self.pred = self.model.predict(self.input_img)
        temp = dict(zip(BREEDS, list(self.pred[0])))
        probabilities = {key: val for key, val in sorted(temp.items(), key = lambda ele: ele[1], reverse = True)}
        prob_dist = {k: round((v*100), 4) for k, v in (list(probabilities.items())[:top])}
        result = []
        for item in prob_dist.items():
            result.append({"class": item[0],
                           "confidence": item[1]})

        # print(prob_dist)
        return result