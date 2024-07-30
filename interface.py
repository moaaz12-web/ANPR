
import tkinter as tk
from tkinter import messagebox
from visualize import process_video_with_license_plate
import cv2
from PIL import Image, ImageTk

class VideoProcessingApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Processing App")

        # Create frames for layout
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(pady=10)

        self.middle_frame = tk.Frame(master)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(pady=10)

        # Label and entry for authorized number plates
        self.label = tk.Label(self.top_frame, text="Enter authorized number plates (separated by commas):")
        self.label.pack(side=tk.LEFT)

        self.number_plates_entry = tk.Entry(self.top_frame)
        self.number_plates_entry.pack(side=tk.LEFT)

        # Process button
        self.process_button = tk.Button(self.middle_frame, text="Process Video", command=self.process_video)
        self.process_button.pack()

        # Video label with margin
        self.video_label = tk.Label(self.middle_frame, padx=20, pady=20)
        self.video_label.pack()

        # Play/pause buttons
        self.play_button = tk.Button(self.bottom_frame, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.bottom_frame, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT)

        # Set initial state of buttons
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

        # Video playback variables
        self.cap = None
        self.video_playing = False

    def process_video(self):
        number_plates = self.number_plates_entry.get().split(",")
        try:
            process_video_with_license_plate('./assets/demo.mp4', './assets/results/test_interpolated.csv', './assets/results/out.mp4', authorized_plates=number_plates)
            messagebox.showinfo("Success", "Video processing completed successfully!")
            self.play_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during video processing: {str(e)}")

    def play_video(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture('./assets/results/out.mp4')
        self.video_playing = True
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.play()

    def play(self):
        if self.video_playing:
            ret, frame = self.cap.read()
            if not ret:
                self.stop()
                return

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)

            self.video_label.config(image=frame)
            self.video_label.image = frame

            self.master.update_idletasks()
            self.master.after(30, self.play)

    def pause_video(self):
        self.video_playing = False
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.video_playing = False
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.video_label.config(image=None)

def main():
    root = tk.Tk()
    app = VideoProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# import tkinter as tk
# from tkinter import messagebox
# from visualize import process_video_with_license_plate
# import cv2
# from PIL import Image, ImageTk

# class VideoProcessingApp:
#     def __init__(self, master):
#         self.master = master
#         master.title("Video Processing App")

#         # Create frames for layout
#         self.top_frame = tk.Frame(master)
#         self.top_frame.pack(pady=10)

#         self.middle_frame = tk.Frame(master)
#         self.middle_frame.pack(pady=10)

#         self.bottom_frame = tk.Frame(master)
#         self.bottom_frame.pack(pady=10)

#         # Label and entry for authorized number plates
#         self.label = tk.Label(self.top_frame, text="Enter authorized number plates (separated by commas):")
#         self.label.pack(side=tk.LEFT)

#         self.number_plates_entry = tk.Entry(self.top_frame)
#         self.number_plates_entry.pack(side=tk.LEFT)

#         # Process button
#         self.process_button = tk.Button(self.middle_frame, text="Process Video", command=self.process_video)
#         self.process_button.pack()

#         # Video label with margin
#         self.video_label = tk.Label(self.middle_frame, padx=10, pady=10)
#         self.video_label.pack()

#         # Play/pause buttons
#         self.play_button = tk.Button(self.bottom_frame, text="Play", command=self.play_video)
#         self.play_button.pack(side=tk.LEFT)

#         self.pause_button = tk.Button(self.bottom_frame, text="Pause", command=self.pause_video)
#         self.pause_button.pack(side=tk.LEFT)

#         # Set initial state of buttons
#         self.play_button.config(state=tk.DISABLED)
#         self.pause_button.config(state=tk.DISABLED)

#         # Video playback variables
#         self.cap = None
#         self.video_playing = False

#     def process_video(self):
#         number_plates = self.number_plates_entry.get().split(",")
#         try:
#             process_video_with_license_plate('./assets/demo.mp4', './assets/results/test_interpolated.csv', './assets/results/out.mp4', authorized_plates=number_plates)
#             messagebox.showinfo("Success", "Video processing completed successfully!")
#             self.play_button.config(state=tk.NORMAL)
#         except Exception as e:
#             messagebox.showerror("Error", f"An error occurred during video processing: {str(e)}")

#     def play_video(self):
#         if self.cap is None:
#             self.cap = cv2.VideoCapture('./assets/results/out.mp4')
#         self.video_playing = True
#         self.play_button.config(state=tk.DISABLED)
#         self.pause_button.config(state=tk.NORMAL)
#         self.play()

#     def play(self):
#         if self.video_playing:
#             ret, frame = self.cap.read()
#             if not ret:
#                 self.stop()
#                 return

#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame = Image.fromarray(frame)
#             frame = ImageTk.PhotoImage(frame)

#             self.video_label.config(image=frame, width=600)  # Adjust the width here
#             self.video_label.image = frame

#             self.master.update_idletasks()
#             self.master.after(30, self.play)

#     def pause_video(self):
#         self.video_playing = False
#         self.play_button.config(state=tk.NORMAL)
#         self.pause_button.config(state=tk.DISABLED)

#     def stop(self):
#         if self.cap is not None:
#             self.cap.release()
#             self.cap = None
#         self.video_playing = False
#         self.play_button.config(state=tk.NORMAL)
#         self.pause_button.config(state=tk.DISABLED)
#         self.video_label.config(image=None)

# def main():
#     root = tk.Tk()
#     app = VideoProcessingApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()
