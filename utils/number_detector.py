# This module is for detecting number in the image and returning the ordered number

from utils.data_loader import load_kor_list

kor_list = load_kor_list() # list of korean characters


def get_linear(x1, y1, x2, y2): # return a, b of y = ax + b
    if (x2 - x1) == 0:
        return 1, 0
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


def is_on_line(box, line): # return True if box is on line else False
    x1, y1, x2, y2 = box.xyxy.tolist()[0]
    x = (x1 + x2) / 2

    line_y = line[0] * x + line[1]

    if line_y < y1 or line_y > y2:
        return False
    else:
        return True


def sort_num(boxes): # return ordered number
    if len(boxes.xywhn.tolist()) == 0:
        return None

    max_idx, min_idx = max_min_idx(boxes)
    max_box = boxes[max_idx]
    min_box = boxes[min_idx]

    x1, y1 = max_box.xywh.tolist()[0][:2]
    x2, y2 = min_box.xywh.tolist()[0][:2]

    line = get_linear(x1, y1, x2, y2)

    box_on_line = []
    rest = []

    for box in boxes:
        if is_on_line(box, line):
            box_on_line.append(box)
        else:
            rest.append(box)

    box_on_line.sort(key=lambda x: x.xywh[0][0])
    rest.sort(key=lambda x: x.xywh[0][0])

    plate_num = ''

    for box in rest:
        plate_num += kor_list[int(box.cls)]

    for box in box_on_line:
        plate_num += kor_list[int(box.cls)]

    if plate_num[0] > '9':
        region_set = ['서울', '경기', '부산', '강원', '충남', '충북', '전남', '전북', '경남', '경북', '제주']
        region = plate_num[:2]
        if region not in region_set:
            plate_num = plate_num[1] + plate_num[0] + plate_num[2:]

        region = plate_num[:2]
        if region not in region_set:
            plate_num = plate_num[2:]

    return plate_num


def max_min_idx(boxes): # return index of max and min box by x
    boxes_x = list(list(zip(*boxes.xywhn.tolist()))[0])
    boxes_rank = boxes_x.copy()
    boxes_rank.sort()
    max_idx = boxes_x.index(boxes_rank[-1])
    min_idx = boxes_x.index(boxes_rank[0])
    return max_idx, min_idx


class DetectNumber: # this class is for detecting number in the image and returning the ordered number
    def __init__(self, model):
        self.model = model

    def get_num_from_img(self, img): # detect number in the image and return ordered number
        result = self.model(img)
        boxes = result[0].boxes
        plate_num = sort_num(boxes)
        return plate_num
