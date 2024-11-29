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

restThreshold = 20  # Threshold for detecting rest
frameDifference = 3  # Number of frames to check for minimal movement (this can be adjusted)

restPositions = []

# Initialize variables to track resting state for each landmark
rest_sum_wrist_left = [0, 0, 0]  # To accumulate position values during rest for left wrist
rest_sum_wrist_right = [0, 0, 0]  # For right wrist
rest_sum_ankle_left = [0, 0, 0]  # For left ankle
rest_sum_ankle_right = [0, 0, 0]  # For right ankle

rest_count = 0  # To count the number of frames during the rest period

# Loop through the list of movements
for index in range(frameDifference, len(movements)):
    # Calculate the differences in positions for each landmark (left wrist, right wrist, left ankle, right ankle)
    difflWrist = []
    diffrWrist = []
    difflAnkle = []
    diffrAnkle = []

    for v in range(0, 3):
        difflWrist.append(movements[index][0][v] - movements[index - frameDifference][0][v])
        diffrWrist.append(movements[index][1][v] - movements[index - frameDifference][1][v])
        difflAnkle.append(movements[index][2][v] - movements[index - frameDifference][2][v])
        diffrAnkle.append(movements[index][3][v] - movements[index - frameDifference][3][v])

    # Calculate the Euclidean distances for each landmark (wrist and ankle)
    distancelWrist = math.sqrt(difflWrist[0] ** 2 + difflWrist[1] ** 2 + difflWrist[2] ** 2)
    distancerWrist = math.sqrt(diffrWrist[0] ** 2 + diffrWrist[1] ** 2 + diffrWrist[2] ** 2)
    distancelAnkle = math.sqrt(difflAnkle[0] ** 2 + difflAnkle[1] ** 2 + difflAnkle[2] ** 2)
    distancerAnkle = math.sqrt(diffrAnkle[0] ** 2 + diffrAnkle[1] ** 2 + diffrAnkle[2] ** 2)

    # If the movement is smaller than the threshold (indicating rest), accumulate the positions
    if distancelWrist < restThreshold and distancerWrist < restThreshold and distancelAnkle < restThreshold and distancerAnkle < restThreshold:
        # Accumulate the positions of the landmarks for the rest interval
        rest_sum_wrist_left[0] += movements[index][0][0]  # Left wrist X
        rest_sum_wrist_left[1] += movements[index][0][1]  # Left wrist Y
        rest_sum_wrist_left[2] += movements[index][0][2]  # Left wrist Z
        
        rest_sum_wrist_right[0] += movements[index][1][0]  # Right wrist X
        rest_sum_wrist_right[1] += movements[index][1][1]  # Right wrist Y
        rest_sum_wrist_right[2] += movements[index][1][2]  # Right wrist Z
        
        rest_sum_ankle_left[0] += movements[index][2][0]  # Left ankle X
        rest_sum_ankle_left[1] += movements[index][2][1]  # Left ankle Y
        rest_sum_ankle_left[2] += movements[index][2][2]  # Left ankle Z
        
        rest_sum_ankle_right[0] += movements[index][3][0]  # Right ankle X
        rest_sum_ankle_right[1] += movements[index][3][1]  # Right ankle Y
        rest_sum_ankle_right[2] += movements[index][3][2]  # Right ankle Z

        rest_count += 1
    else:
        # If a rest interval ended (movement exceeds the threshold), calculate the average and store it
        if rest_count > 0:
            # Calculate the average for each landmark
            average_rest_wrist_left = [rest_sum_wrist_left[0] / rest_count, 
                                       rest_sum_wrist_left[1] / rest_count, 
                                       rest_sum_wrist_left[2] / rest_count]
            
            average_rest_wrist_right = [rest_sum_wrist_right[0] / rest_count, 
                                        rest_sum_wrist_right[1] / rest_count, 
                                        rest_sum_wrist_right[2] / rest_count]
            
            average_rest_ankle_left = [rest_sum_ankle_left[0] / rest_count, 
                                       rest_sum_ankle_left[1] / rest_count, 
                                       rest_sum_ankle_left[2] / rest_count]
            
            average_rest_ankle_right = [rest_sum_ankle_right[0] / rest_count, 
                                        rest_sum_ankle_right[1] / rest_count, 
                                        rest_sum_ankle_right[2] / rest_count]

            # Store the average positions for the rest period
            restPositions.append({
                'left_wrist': average_rest_wrist_left,
                'right_wrist': average_rest_wrist_right,
                'left_ankle': average_rest_ankle_left,
                'right_ankle': average_rest_ankle_right
            })
            
            # Reset rest accumulation variables for the next interval
            rest_sum_wrist_left = [0, 0, 0]
            rest_sum_wrist_right = [0, 0, 0]
            rest_sum_ankle_left = [0, 0, 0]
            rest_sum_ankle_right = [0, 0, 0]
            rest_count = 0

# If there's an ongoing rest period at the end of the loop, store the average position
if rest_count > 0:
    average_rest_wrist_left = [rest_sum_wrist_left[0] / rest_count, 
                               rest_sum_wrist_left[1] / rest_count, 
                               rest_sum_wrist_left[2] / rest_count]
    
    average_rest_wrist_right = [rest_sum_wrist_right[0] / rest_count, 
                                rest_sum_wrist_right[1] / rest_count, 
                                rest_sum_wrist_right[2] / rest_count]
    
    average_rest_ankle_left = [rest_sum_ankle_left[0] / rest_count, 
                               rest_sum_ankle_left[1] / rest_count, 
                               rest_sum_ankle_left[2] / rest_count]
    
    average_rest_ankle_right = [rest_sum_ankle_right[0] / rest_count, 
                                rest_sum_ankle_right[1] / rest_count, 
                                rest_sum_ankle_right[2] / rest_count]
    
    # Store the final average positions for the rest period
    restPositions.append({
        'left_wrist': average_rest_wrist_left,
        'right_wrist': average_rest_wrist_right,
        'left_ankle': average_rest_ankle_left,
        'right_ankle': average_rest_ankle_right
    })

# Print the rest positions
print("Rest Positions:")
print(len(restPositions))