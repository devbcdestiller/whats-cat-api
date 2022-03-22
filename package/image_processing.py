import numpy as np

class ImageProcessing():
    def __init__(self, img):
        self.img = img
        pass

    def image_to_array(self, img_width=300, img_height=300):
        img = self.img.resize((img_width, img_height), resample=0, box=None)
        img = np.array(img)
        img = img / 255.0
        return np.array([img])