import pyttsx3
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/CH"
counter = 0
insert_text = ""
letter = ""
labels = ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "CH"]

engine = pyttsx3.init()

while True:
    text = ""
    success, img = cap.read()

    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                      (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

        if labels[index] == "CH":
            if letter == "CH":
                letter = ""
            elif letter[0:2] == "CH":
                insert_text = insert_text + letter[2]
                engine.say(insert_text)
                text = insert_text
                # print(letter[0])
                letter = ""
                # cv2.putText(gesture_window, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
                # cv2.imshow("Gesture Text", gesture_window)
            else:
                insert_text = insert_text + letter[0]
                engine.say(insert_text)
                text = insert_text
                # print(letter[0])
                letter = ""
                # cv2.putText(gesture_window, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
                # cv2.imshow("Gesture Text", gesture_window)
        # gesture_window = np.ones((100, 800, 3), dtype="uint8") * 255

        letter = letter + labels[index]
        print(letter)
        cv2.rectangle(imgOutput, (x - offset, y - offset),
                      (x + w + offset, y + h + offset), (255, 0, 255), 4)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)

    engine.runAndWait()
