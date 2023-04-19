# This file contains the class for detecting and cropping the license plate from the image

import re
import cv2

from utils.model_loader import load_model
from utils.plate_detector import DetectPlate
from utils.plate_warper import WarpPlate
from utils.number_detector import DetectNumber

regex = '([가-힣]{2}[0-9]{2}[가-힣]{1}[0-9]{4})|([0-9]{2,3}[가-힣]{1}[0-9]{4})'  # regex for license plate number
output_regex = '([0-9]{2,3}[가-힣]{1}[0-9]{4})'  # regex for wanted license plate number

# set the model names
plate_detect_model = "plate_detect_v1"
vertex_detect_model = "vertex_detect_v1"
syllable_detect_model = "syllable_detect_v1"

# load the models
plate_detector = DetectPlate(load_model(plate_detect_model))
vertex_detector = WarpPlate(load_model(vertex_detect_model))
syllable_detector = DetectNumber(load_model(syllable_detect_model))


def get_num(img, save=False, save_not_detected=False, save_path='./temp_data/',
            save_name='temp'):  # return the license plate number
    if save_path[-1] != '/':  # add '/' to the end of the path if it doesn't exist
        save_path += '/'
    if save_name[-1] == '/':  # remove '/' from the end of the name if it exists
        save_name = save_name[:-1]

    cropped_img = plate_detector.detect_and_crop(img)  # crop the image
    warped_img = vertex_detector.detect_and_warp(cropped_img)  # warp the image

    if cropped_img is None:
        print("cropped_img is None")
    if warped_img is None:
        print("warped_img is None")

    if cropped_img is not None:
        res1 = syllable_detector.get_num_from_img(cropped_img)  # get the number from the cropped image
    else:
        res1 = None

    if warped_img is not None:
        res2 = syllable_detector.get_num_from_img(warped_img)  # get the number from the warped image
    else:
        res2 = None

    result = confirm_num(res1, res2)  # return the number that is confirmed to be the license plate number

    if save:
        cv2.imwrite(save_path + "origin_" + save_name + ".jpg", img)
        cv2.imwrite(save_path + "cropped_" + save_name + ".jpg", cropped_img)
        cv2.imwrite(save_path + "warped_" + save_name + ".jpg", warped_img)

    elif result is None and save_not_detected:
        if warped_img is not None:
            cv2.imwrite(save_path + save_name + ".jpg", warped_img)
        elif cropped_img is not None:
            cv2.imwrite(save_path + save_name + ".jpg", cropped_img)
        else:
            cv2.imwrite(save_path + save_name + ".jpg", img)

    return result


def confirm_num(plate_num1, plate_num2, mask=True):  # return the confirmed license plate number
    if plate_num1 is None:
        plate_num1 = ''
    if plate_num2 is None:
        plate_num2 = ''

    m1 = re.fullmatch(regex, plate_num1)
    m2 = re.fullmatch(regex, plate_num2)

    if plate_num1 == plate_num2 and m1 is not None:
        plate_num = plate_num1

    else:
        if m1 is not None:
            plate_num = plate_num1
        elif m2 is not None:
            plate_num = plate_num2
        else:
            return None

    if mask:
        plate_num = re.search(output_regex, plate_num).group()

    return plate_num
