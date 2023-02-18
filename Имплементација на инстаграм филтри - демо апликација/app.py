# USAGE: python finish.py
import cv2
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
import filters
import time

face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile = cv2.CascadeClassifier("smile.xml")
hat = cv2.imread("witch.png")

top = tk.Tk()

top.geometry("650x150")

usage = Label(top, text="Ако изберете некој од првите 4 филтри, ќе бидете фотографирани за 4 секунди!"
                        "\nАко изберет од останатите, ќе се вклучи камера да ве снима!").place(x=95, y=60)

top.mainloop()


def takePicture():
    cam = cv2.VideoCapture(2)
    time.sleep(4)
    result, image = cam.read()
    return image


def selection():
    fig = plt.figure()
    value = int(v.get())
    if value == 1 or value == 2 or value == 3 or value == 4:
        image = takePicture()
        if value == 1:
            img_1 = filters.Sharpen(image)
            img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
            plt.xticks([]), plt.yticks([]), plt.imshow(img_1)
            fig.suptitle("Sharpen filter")
            plt.show()
        elif value == 2:
            img_2 = filters.Gingham(image)
            img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2RGB)
            plt.xticks([]), plt.yticks([]), plt.imshow(img_2)
            fig.suptitle("Gingham filter")
            plt.show()
        elif value == 3:
            img_3 = filters.Sepia(image)
            img_3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2RGB)
            plt.xticks([]), plt.yticks([]), plt.imshow(img_3)
            fig.suptitle("Sepia filter")
            plt.show()
        elif value == 4:
            img_4 = filters.Invert(image)
            img_4 = cv2.cvtColor(img_4, cv2.COLOR_BGR2RGB)
            plt.xticks([]), plt.yticks([]), plt.imshow(img_4)
            fig.suptitle("Invert filter")
            plt.show()
    else:
        webcam = cv2.VideoCapture(2)
        while True:
            res, im = webcam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face.detectMultiScale(gray, 1.3, 5)
            smiles = smile.detectMultiScale(gray, 1.8, 20)
            if value == 5:
                im = filters.Halloween(hat, im, faces)
                cv2.imshow('Halloween filter', im)
            elif value == 6:
                im = filters.Smile(faces, im, smiles)
                cv2.imshow('Smile filter', im)

            key = cv2.waitKey(30)
            if key == 27:
                cv2.destroyAllWindows()
                break


window = tk.Tk()
window.geometry("300x221")

window.title("Choose filter:")
values = {"Sharpen filter": "1",
          "Gingham filter": "2",
          "Sepia filter": "3",
          "Invert Effect": "4",
          "Halloween filter": "5",
          "How good is your smile": "6"}

v = StringVar(window, "0")
colors = ["#98FF98", "#7BE27D", "#5FC663", "#41AA4A", "#1E8F31", "#007417"]
i = 0
for (text, value) in values.items():
    Radiobutton(window, text=text,
                variable=v,
                value=value, indicator=0,
                background=colors[i], command=selection).pack(fill=X, ipady=6)
    i = i + 1
window.mainloop()
