# This file contains the class for detecting and cropping the license plate from the image

def crop_img(img, result):  # img: image to crop, result: result of the model
    if len(result[0].boxes) == 0:  # if there is no box
        return None
    elif len(result[0].boxes) > 1:  # if there are more than 1 box
        return None
    boxes = result[0].boxes[0]
    box = boxes.xyxy.tolist()[0]
    x1, y1, x2, y2 = box
    cropped_img = img[int(y1):int(y2), int(x1):int(x2)]
    return cropped_img


class DetectPlate:  # This class is for detecting and cropping the license plate from the image
    def __init__(self, model):
        self.model = model

    def detect_and_crop(self, img):  # return cropped image
        result = self.model(img)
        cropped_img = crop_img(img, result)
        return cropped_img
