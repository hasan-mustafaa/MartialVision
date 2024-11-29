import cv2 as cv
from cvzone.PoseModule import PoseDetector

cap = cv.VideoCapture("Form1.mp4")

detector = PoseDetector()

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxinfo = detector.findPosition(img)
    cv.imshow("Image", img)
    cv.waitKey(1)