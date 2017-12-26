import cv2
import imutils as imutils
import numpy as np
from imutils import contours
from main.detect_letter_with_turning import resolve_symbol

# load the reference MICR image from disk, convert it to grayscale,
# and threshold it, such that the digits appear as *white* on a
# *black* background

SYMBOL_TEMP_FILE = 'symbol.png'


def recognize_captcha(file_name, mode='usual'):
    ref = cv2.imread(file_name)
    ref = imutils.resize(ref, width=400)
    # cv2.imshow("Output", ref)
    # cv2.waitKey(0)

    if mode == 'usual':
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    elif mode == 'splashing':
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.adaptiveThreshold(ref, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 51, 2)
        kernel = np.ones((6,6),np.uint8)
        ref = cv2.morphologyEx(ref, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((4,4),np.uint8)
        ref = cv2.erode(ref, kernel, iterations = 1)
    elif mode == 'noise':
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Output", ref)
        cv2.waitKey(0)
        ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cv2.imshow("Output", ref)
        cv2.waitKey(0)
        kernel = np.ones((3, 3), np.uint8)
        ref = cv2.morphologyEx(ref, cv2.MORPH_OPEN, kernel)
    elif mode == 'corn':
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = np.ones((3, 3), np.uint8)
        ref = cv2.morphologyEx(ref, cv2.MORPH_CLOSE, kernel)
    elif mode == 'mail':
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = np.ones((3, 3), np.uint8)
        ref = cv2.morphologyEx(ref, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((5, 5), np.uint8)
        ref = cv2.morphologyEx(ref, cv2.MORPH_CLOSE, kernel)
    elif mode == 'stones':
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = np.ones((5, 5), np.uint8)
        ref = cv2.dilate(ref, kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        ref = cv2.erode(ref, kernel, iterations=1)
    else:
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cv2.imshow("Output", ref)
    cv2.waitKey(0)

    # find contours in the MICR image (i.e,. the outlines of the
    # characters) and sort them from left to right
    refCnts = cv2.findContours(ref.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
    refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]

    # create a clone of the original image so we can draw on it
    clone = np.dstack([ref.copy()] * 3)

    # loop over the (sorted) contours
    captcha = ''
    for c in refCnts:
        # compute the bounding box of the contour and draw it on our image
        if 400 < cv2.contourArea(c) < 2000:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.imwrite(SYMBOL_TEMP_FILE, clone[y:(y + h), x:(x + w)])
            captcha += resolve_symbol(SYMBOL_TEMP_FILE)

    return captcha


