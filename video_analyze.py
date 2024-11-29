import cv2 as cv
from cvzone.PoseModule import PoseDetector
import math

def detect_rest_positions(video_file):
    cap = cv.VideoCapture(video_file)
    detector = PoseDetector()

    movements = []

    # Capture the frames and extract movements
    while True:
        success, img = cap.read()
        if not success:
            break
        img = detector.findPose(img)
        lmList, bboxinfo = detector.findPosition(img)
        if bboxinfo:
            left_wrist = lmList[15]
            right_wrist = lmList[16]
            movements.append([left_wrist, right_wrist])

    cap.release()

    restThreshold = 14  # Threshold for detecting rest 
    frameDifference = 11  # Number of frames to check for minimal movement (this can be adjusted)

    restPositions = []
    restPositions.append({'left_wrist': 0, 'right_wrist': 0})

    # Initialize variables to track resting state for each wrist
    rest_sum_wrist_left = [0, 0, 0]  # To accumulate position values during rest for left wrist
    rest_sum_wrist_right = [0, 0, 0]  # For right wrist

    rest_count = 0  # To count the number of frames during the rest period

    # Loop through the list of movements
    for index in range(frameDifference, len(movements)):
        # Calculate the differences in positions for each wrist
        difflWrist = []
        diffrWrist = []

        for v in range(0, 3):
            difflWrist.append(movements[index][0][v] - movements[index - frameDifference][0][v])
            diffrWrist.append(movements[index][1][v] - movements[index - frameDifference][1][v])

        # Calculate the Euclidean distances for each wrist
        distancelWrist = math.sqrt(difflWrist[0] ** 2 + difflWrist[1] ** 2 + difflWrist[2] ** 2)
        distancerWrist = math.sqrt(diffrWrist[0] ** 2 + diffrWrist[1] ** 2 + diffrWrist[2] ** 2)

        # If the movement is smaller than the threshold (indicating rest), accumulate the positions
        if distancelWrist < restThreshold and distancerWrist < restThreshold:
            # Accumulate the positions of the wrists for the rest interval
            rest_sum_wrist_left[0] += movements[index][0][0]  # Left wrist X
            rest_sum_wrist_left[1] += movements[index][0][1]  # Left wrist Y
            rest_sum_wrist_left[2] += movements[index][0][2]  # Left wrist Z

            rest_sum_wrist_right[0] += movements[index][1][0]  # Right wrist X
            rest_sum_wrist_right[1] += movements[index][1][1]  # Right wrist Y
            rest_sum_wrist_right[2] += movements[index][1][2]  # Right wrist Z

            rest_count += 1
        else:
            # If a rest interval ended (movement exceeds the threshold), calculate the average and store it
            if rest_count > 0:
                # Calculate the average for each wrist
                average_rest_wrist_left = [rest_sum_wrist_left[0] / rest_count, 
                                           rest_sum_wrist_left[1] / rest_count, 
                                           rest_sum_wrist_left[2] / rest_count]

                average_rest_wrist_right = [rest_sum_wrist_right[0] / rest_count, 
                                            rest_sum_wrist_right[1] / rest_count, 
                                            rest_sum_wrist_right[2] / rest_count]

                # Store the average positions for the rest period
                restPositions.append({
                    'left_wrist': average_rest_wrist_left,
                    'right_wrist': average_rest_wrist_right
                })
                
                # Reset rest accumulation variables for the next interval
                rest_sum_wrist_left = [0, 0, 0]
                rest_sum_wrist_right = [0, 0, 0]
                rest_count = 0

    # If there's an ongoing rest period at the end of the loop, store the average position
    if rest_count > 0:
        average_rest_wrist_left = [rest_sum_wrist_left[0] / rest_count, 
                                   rest_sum_wrist_left[1] / rest_count, 
                                   rest_sum_wrist_left[2] / rest_count]
        
        average_rest_wrist_right = [rest_sum_wrist_right[0] / rest_count, 
                                    rest_sum_wrist_right[1] / rest_count, 
                                    rest_sum_wrist_right[2] / rest_count]

        # Store the final average positions for the rest period
        restPositions.append({
            'left_wrist': average_rest_wrist_left,
            'right_wrist': average_rest_wrist_right
        })

    return restPositions