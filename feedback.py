import cv2 as cv
from video_analyze import detect_rest_positions
import math

# Step 1: Analyze videos
video_file = "Form1.mp4"
video_positions = detect_rest_positions(video_file)

video_file = "Demo2.mp4"
user_positions = detect_rest_positions(video_file)

feedback = ""

def calculate_euclidean_distance(pos1, pos2):
    """Calculate the Euclidean distance between two 3D points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)

if len(video_positions) != len(user_positions):
    feedback = "Mismatch in number of rest positions. Ensure both forms have similar timing and pauses."
else:
    total_difference = 0
    total_positions = len(video_positions)

    # Loop through positions to calculate differences
    for index in range(total_positions):
        video_fist = video_positions[index]['left_wrist']  # Assuming only left wrist
        user_fist = user_positions[index]['left_wrist']

        # Calculate Euclidean distance for left fist (you can extend this for right if needed)
        difference = calculate_euclidean_distance(video_fist, user_fist)
        total_difference += difference

    # Calculate average difference
    average_difference = total_difference / total_positions

    # Determine similarity percentage (lower average difference = higher similarity)
    max_allowable_difference = 50  # Adjust this threshold based on acceptable tolerance
    similarity_percentage = max(0, 100 - (average_difference / max_allowable_difference) * 100)

    # Provide feedback
    if similarity_percentage > 90:
        feedback = f"Great job! Your movements are {similarity_percentage:.2f}% similar to the reference video."
    elif similarity_percentage > 75:
        feedback = f"Good effort! Your movements are {similarity_percentage:.2f}% similar. Focus on refining your pauses and positions."
    else:
        feedback = f"Needs improvement. Your movements are only {similarity_percentage:.2f}% similar. Work on matching the reference video more closely."

print(feedback)