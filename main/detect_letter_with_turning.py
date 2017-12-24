import pytesseract as pt
import imutils
import numpy as np
import os
import operator
import cv2
from PIL import Image

TEMPLATE_FILE_NAME = 'template.png'
TEMP_FILE_NAME = 'temp.png'
IMAGE_IN_TEMPLATE = 'out.png'


def insert_into_template(file_name, angle):
    im = Image.open(TEMPLATE_FILE_NAME)
    newImage = Image.open(file_name)
    im.paste(newImage, (318, 80))
    im.save(IMAGE_IN_TEMPLATE)


def is_valid_ascii_code(symbol):
    ascii_code = ord(symbol)
    if (47 < ascii_code < 58) or (64 < ascii_code < 91) or (96 < ascii_code < 123):
        return True
    else:
        return False


def resolve_symbol(file_name):
    image = cv2.imread(file_name)
    # cv2.imshow("Output", image)
    # cv2.waitKey(0)
    symbols = {}

    for angle in np.arange(0, 360, 1):
        rotated = imutils.rotate_bound(image, angle)
        cv2.imwrite(TEMP_FILE_NAME, rotated)
        insert_into_template(TEMP_FILE_NAME, angle)
        text = pt.image_to_string(Image.open(IMAGE_IN_TEMPLATE))
        print(str(angle) + ': ' + text)

        length = len(text)
        if length > 4 and text[0] == 'F' and text[1] == 'F' and text[length - 1] == 'F' and text[length - 2] == 'F':
            detection = text[2:-2].replace(" ", "")
            if len(detection) == 1:
                key = text[2]
                print(key)
                if is_valid_ascii_code(key):
                    if key in symbols.keys():
                        symbols[key] += 1
                    else:
                        symbols[key] = 1

    os.remove(TEMP_FILE_NAME)
    os.remove(IMAGE_IN_TEMPLATE)

    return max(symbols.items(), key=operator.itemgetter(1))[0]



