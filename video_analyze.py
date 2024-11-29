import cv2 as cv
from cvzone.PoseModule import PoseDetector
import math

cap = cv.VideoCapture("Form1.mp4")

detector = PoseDetector()

movements = []

while True:
    success, img = cap.read()
    if not success:
        break
    img = detector.findPose(img)
    lmList, bboxinfo = detector.findPosition(img)
    if bboxinfo:
        left_wrist = lmList[15]
        right_wrist = lmList[16]
        left_ankle = lmList[27]
        right_ankle = lmList[28]
        movements.append([left_wrist, right_wrist, left_ankle, right_ankle])
        
    cv.imshow("Image", img)
    cv.waitKey(1)

restThreshold = 10  # Threshold for detecting rest
frameDifference = 5  # Number of frames to compare for detecting rest

newMovements = []
rest_positions = []  # To accumulate rest positions

# Initialize variables to track resting state
rest_counter = 0
rest_sum = [0, 0, 0]  # To accumulate position values during rest
rest_count = 0  # To count the number of frames during the rest period

for index in range(frameDifference, len(movements)):
    difflWrist = []
    diffrWrist = []
    difflAnkle = []
    diffrAnkle = []

    # Calculate the difference in positions
    for v in range(0, 3):
        difflWrist.append(movements[index][v] - movements[index - frameDifference][v])
        diffrWrist.append(movements[index][v] - movements[index - frameDifference][v])
        difflAnkle.append(movements[index][v] - movements[index - frameDifference][v])
        diffrAnkle.append(movements[index][v] - movements[index - frameDifference][v])

    # Calculate the distances (Euclidean distance in 3D space)
    distancelWrist = math.sqrt(difflWrist[0] ** 2 + difflWrist[1] ** 2 + difflWrist[2] ** 2)
    distancerWrist = math.sqrt(diffrWrist[0] ** 2 + diffrWrist[1] ** 2 + diffrWrist[2] ** 2)
    distancelAnkle = math.sqrt(difflAnkle[0] ** 2 + difflAnkle[1] ** 2 + difflAnkle[2] ** 2)
    distancerAnkle = math.sqrt(diffrAnkle[0] ** 2 + diffrAnkle[1] ** 2 + diffrAnkle[2] ** 2)

    # Check if the movement is smaller than the threshold (indicating rest)
    if distancelWrist < restThreshold and distancerWrist < restThreshold and distancelAnkle < restThreshold and distancerAnkle < restThreshold:
        rest_counter += 1
        
        # Accumulate positions during the resting period
        rest_sum[0] += movements[index][0]  # Left wrist X
        rest_sum[1] += movements[index][1]  # Left wrist Y
        rest_sum[2] += movements[index][2]  # Left wrist Z
        
        rest_count += 1

        # If we have enough frames of rest, store the average position
        if rest_counter >= frameDifference:
            average_rest_position = [rest_sum[0] / rest_count, rest_sum[1] / rest_count, rest_sum[2] / rest_count]
            rest_positions.append(average_rest_position)
            rest_counter = 0  # Reset counter
            rest_sum = [0, 0, 0]  # Reset accumulated sum
            rest_count = 0  # Reset count for averaging
    else:
        # If movement is detected, store the current positions (this is the new movement)
        newMovements.append(movements[index])

# After the loop ends, if there are any remaining rest positions, append them
if rest_counter > 0:
    average_rest_position = [rest_sum[0] / rest_count, rest_sum[1] / rest_count, rest_sum[2] / rest_count]
    rest_positions.append(average_rest_position)

# Print the new movements and the rest positions
print("New Movements:")
print(newMovements)

print("Rest Positions:")
print(rest_positions)