import cv2 as cv
from video_analyze import detect_rest_positions
import math

def evaluate_movements(video_positions, user_positions):
    if len(video_positions) > len(user_positions):
        return "You are doing it too quickly, please be more firm."
    elif len(video_positions) < len(user_positions):
        return "Too sluggish, be quicker."
    else:
        differences = 0
        for index in range(1, len(video_positions)):
            # Calculate distances between consecutive positions for both videos
            video_distance = math.sqrt(
                (video_positions[index]['left_wrist'][0] - video_positions[index - 1]['left_wrist'][0]) ** 2 +
                (video_positions[index]['left_wrist'][1] - video_positions[index - 1]['left_wrist'][1]) ** 2 +
                (video_positions[index]['left_wrist'][2] - video_positions[index - 1]['left_wrist'][2]) ** 2
            )
            user_distance = math.sqrt(
                (user_positions[index]['left_wrist'][0] - user_positions[index - 1]['left_wrist'][0]) ** 2 +
                (user_positions[index]['left_wrist'][1] - user_positions[index - 1]['left_wrist'][1]) ** 2 +
                (user_positions[index]['left_wrist'][2] - user_positions[index - 1]['left_wrist'][2]) ** 2
            )
            differences += abs(video_distance - user_distance)
        
        # Calculate the average difference
        avg_difference = differences / len(video_positions)
        difference_percent = (avg_difference / 400) * 100
            # Generate feedback based on the percentage of inaccuracy
        if difference_percent < 10:
            quote = "Excellent! You're almost in perfect sync with the reference."
        elif difference_percent < 25:
            quote = "Good job! There's room for improvement, but you're on the right track."
        elif difference_percent < 50:
            quote = "Decent effort, but there are noticeable differences. Keep practicing!"
        else:
            quote = "The accuracy needs improvement. Focus on refining your movements."

        return f"Inaccuracy: {difference_percent:.2f}% - {quote}"