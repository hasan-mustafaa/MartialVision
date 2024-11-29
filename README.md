# MartialVision

An AI-powered platform designed to enhance martial arts practice by analyzing and grading movements. The system uses computer vision to compare a user's performance with tutorial videos and provides detailed feedback to help them master their skills.

## Key Features:

### Tutorial Playback: 
 - Plays segmented videos of martial arts movements for users to follow.
### User Video Capture:
 - Records the user's performance of the selected martial arts section.
### AI-Powered Grading
 - Uses OpenCV to analyze and compare the user's movements with the tutorial.
 - Splices videos into comparable sections for accurate grading.
 - Scores performance based on posture, precision, and timing.
### Cumulative Scoring and Feedback
 - Provides segment-wise scores and a final cumulative score.
 - Highlights areas of improvement using visual feedback (e.g., heatmaps, overlays).

## How It Works
### Step 1: Choose a Tutorial
 - Select a specific martial arts technique or movement to practice.
### Step 2: Record Performance
 - Perform the action while the system records your movements via webcam or phone camera.
### Step 3: AI Analysis
 - OpenCV tracks body motion and compares it with the tutorial video.
 - Identifies deviations in joint angles, timing, and accuracy.
### Step 4: Get Your Score
 - Receive a detailed breakdown of your performance:
 - Segment scores (e.g., footwork, punches, kicks).
 - Cumulative overall score.
 - Suggestions for improvement are displayed.
