# Description: Load data from txt file

def get_data_from_txt(path): # path: txt file path
    result = []

    with open(path, 'r', encoding='UTF8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        result.append(line)

    return result


def load_kor_list(): # return: list of korean characters
    return get_data_from_txt('./utils/data/kor_list.txt')


def load_plate_list(): # return: list of plate numbers
    return get_data_from_txt('./utils/data/plate_list.txt')


def add_to_plate_list(plate_num): # plate_num: plate number to add to plate_list.txt
    with open('./utils/data/plate_list.txt', 'a', encoding='UTF8') as f:
        f.write(plate_num + '\n')
