import tkinter as tk
from tkinter import filedialog, messagebox
from video_analyze import detect_rest_positions  # Your implementation here
from feedback import evaluate_movements  # Your implementation here

def analyze_videos():
    # Prompt user to select the reference video
    video_file_1 = filedialog.askopenfilename(
        title="Select Reference Video",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if not video_file_1:
        messagebox.showerror("Error", "No reference video selected.")
        return

    # Prompt user to select the user's demo video
    video_file_2 = filedialog.askopenfilename(
        title="Select User Demo Video",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if not video_file_2:
        messagebox.showerror("Error", "No user demo video selected.")
        return

    # Analyze the positions using the detect_rest_positions function
    try:
        # You need to implement the logic of detect_rest_positions to return a list of positions
        video_positions = detect_rest_positions(video_file_1)
        user_positions = detect_rest_positions(video_file_2)

        # Get feedback using the evaluate_movements function
        # You need to define how feedback is generated
        feedback = evaluate_movements(video_positions, user_positions)
        
        feedback_label.config(text=f"Feedback: {feedback}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Martial Vision Feedback")

# Set the window size (width x height)
root.geometry("800x600")  # Adjust this as needed
root.config(bg="#f0f0f0")  # Set a light background color

# Use a frame to hold widgets and give it padding
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(fill="both", expand=True, padx=20, pady=20)

# Create and style the title label
title_label = tk.Label(frame, text="Martial Vision Feedback", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=20)

# Add a button to trigger video analysis with custom styling
analyze_button = tk.Button(frame, text="Analyze Videos", command=analyze_videos, font=("Helvetica", 16), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
analyze_button.pack(pady=20)

# Label to display feedback with customized font and padding
feedback_label = tk.Label(frame, text="Feedback will appear here.", font=("Helvetica", 16), wraplength=600, justify="center", bg="#f0f0f0", fg="#333")
feedback_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()