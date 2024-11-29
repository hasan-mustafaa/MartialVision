import cv2 as cv
from video_analyze import detect_rest_positions

# Step 1: Analyze "Form1.mp4"cl
video_file = "Form1.mp4"
rest_positions_form1 = detect_rest_positions(video_file)

video_file = "Demo2.mp4"
rest_positions_form1 = detect_rest_positions(video_file)