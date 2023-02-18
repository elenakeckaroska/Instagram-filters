import random
import time
import cv2
import numpy as np


def brightness_contrast(img, alpha=1.0, beta=0):
    img_contrast = img * (alpha)
    img_bright = img_contrast + (beta)
    img_bright = np.clip(img_bright, 0, 255)
    img_bright = img_bright.astype(np.uint8)
    return img_bright


def hue_saturation(img_rgb, alpha=1, beta=1):
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
    hue = img_hsv[:, :, 0]
    saturation = img_hsv[:, :, 1]
    hue = np.clip(hue * alpha, 0, 179)
    saturation = np.clip(saturation * beta, 0, 255)
    img_hsv[:, :, 0] = hue
    img_hsv[:, :, 1] = saturation
    img_transformed = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return img_transformed


def Sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img_sharpen = cv2.filter2D(img, -1, kernel)
    return img_sharpen


def Gingham(img, hue=1.1, saturation=0.9, contrast=1.1, brightness=-20):
    img = hue_saturation(img, hue, saturation)
    img = brightness_contrast(img, contrast, brightness)
    return img


def Sepia(img):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]
    img1 = np.zeros((height, width, 3), np.uint8)
    for py in range(height):
        for px in range(width):
            b = img[py, px][0]
            g = img[py, px][1]
            r = img[py, px][2]

            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)

            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255
            img1[py, px] = (tb, tg, tr)
    return img1


def Invert(img):

    inv = cv2.bitwise_not(img)
    return inv


def Halloween(witch, img, faces):
    witch_gray = cv2.cvtColor(witch, cv2.COLOR_BGR2GRAY)

    ret, original_mask = cv2.threshold(witch_gray, 10, 255, cv2.THRESH_BINARY_INV)
    original_mask_inv = cv2.bitwise_not(original_mask)
    original_witch_h, original_witch_w, witch_channels = witch.shape
    img_h, img_w = img.shape[:2]

    for (x, y, w, h) in faces:

        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_w
        face_y1 = y

        witch_width = int(1.5 * face_w)
        witch_height = int(witch_width * original_witch_h / original_witch_w)

        witch_x1 = face_x2 - int(face_w / 2) - int(witch_width / 2)
        witch_x2 = witch_x1 + witch_width
        witch_y1 = face_y1 - int(face_h * 1.25)
        witch_y2 = witch_y1 + witch_height

        if witch_x1 < 0:
            witch_x1 = 0
        if witch_y1 < 0:
            witch_y1 = 0
        if witch_x2 > img_w:
            witch_x2 = img_w
        if witch_y2 > img_h:
            witch_y2 = img_h

        witch_width = witch_x2 - witch_x1
        witch_height = witch_y2 - witch_y1

        witch = cv2.resize(witch, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
        mask = cv2.resize(original_mask, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
        mask_inv = cv2.resize(original_mask_inv, (witch_width, witch_height), interpolation=cv2.INTER_AREA)

        roi = img[witch_y1:witch_y2, witch_x1:witch_x2]

        roi_bg = cv2.bitwise_and(roi, roi, mask=mask)

        roi_fg = cv2.bitwise_and(witch, witch, mask=mask_inv)

        dst = cv2.add(roi_bg, roi_fg)

        img[witch_y1:witch_y2, witch_x1:witch_x2] = dst

    return img


def Smile(faces, im, smiles):
    for x, y, w, h in faces:
        img = cv2.rectangle(im, (x, y), (x + (w + 20), y + (h - 400)), (40, 24, 14), -1)
        for x1, y1, w1, h1 in smiles:
            img = cv2.rectangle(im, (x1, y1), (x1 + w1, y1 + h1), (40, 24, 14), 3)
            Smile_meter(x, y, im)

    return im


num = 0


def Smile_meter(x, y, im):
    global num
    if num > 100:
        r = str(random.randint(0, 100))
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (250, 244, 241)
        text = cv2.putText(im, "Your smile is", (int(x) + 15, int(y) - 70), font, 1, color, 4, cv2.LINE_AA)
        text = cv2.putText(im, r + "%/100%", (int(x) + 50, int(y) - 20), font, 1, color, 4, cv2.LINE_AA)
        time.sleep(7)
        num = 0
        return num
    else:
        r = str(random.randint(0, 100))
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (250, 244, 241)
        text = cv2.putText(im, "Your smile is", (int(x) + 15, int(y) - 70), font, 1, color, 4, cv2.LINE_AA)
        text = cv2.putText(im, r + "%/100%", (int(x) + 50, int(y) - 20), font, 1, color, 4, cv2.LINE_AA)
        num = num + 5
        return num
