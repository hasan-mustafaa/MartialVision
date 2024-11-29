import cv2 as cv
from video_analyze import detect_rest_positions

# Step 1: Analyze "Form1.mp4"cl
video_file = "Form1.mp4"
video_positions = detect_rest_positions(video_file)

video_file = "Demo2.mp4"
user_positions = detect_rest_positions(video_file)

feedback = ""

if len(video_positions) > len(user_positions):
    feedback = "You are doing it too quickly, please be more firm"
elif len(video_positions) < len(user_positions):
    feedback = "Too sluggish, be quicker"
else:
    for index in range(1, len(video_positions)):
