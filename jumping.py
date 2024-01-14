import cv2
import math
from tkinter import *
from PIL import Image, ImageTk
import mediapipe as md

# Importing necessary libraries

md_drawing = md.solutions.drawing_utils
md_drawing_style = md.solutions.drawing_styles
md_pose = md.solutions.pose

count = 0
position = None

cap = cv2.VideoCapture(0)
video_file = None

# Initializing variables and capturing video

root = Tk()
root.title("JUMPING JACK")
root.geometry('500x400+268+82')
root.configure(bg="#FFD700")

# Creating the Tkinter window

f1= LabelFrame(root, bg="#0000FF").place(relx=0.5,rely=0.5) #this is vid background

label = Label(root, text="Jumping Jack Count: 0", font=("Arial", 24))
label.pack(pady=10)

# Creating labels for displaying information

# Label(root,text="2021-MC-06 HASSAN ALI ",font=("Calibri",20),bg="#0000FF",fg="#fffdd0").place(relx=0.75,rely=0.2)
# Label(root,text="2021-MC-08 MUEEZ ALI",font=("Calibri",20),bg="#0000FF",fg="#fffdd0").place(relx=0.75,rely=0.25)

# Creating labels for authors' information

video_label = Label(root)
video_label.pack()

# Creating a label for displaying video

def close():
    root.destroy()

# Function to close the application

Button(f1, text="Exit the Application", bg='#fffdd0', fg='red', font=("Calibri", 14, "bold"), command=close).place(relx=0.11, rely=0.8, anchor ="center")

# Creating an exit button

pose = md_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.7
)

# Initializing the Pose object for pose estimation

def update_jump():
    global count
    label.config(text=f"JUMPING JACK: {count}")
    label.after(1000, update_jump)

# Function to update the jumping jack count every second

def process_frame():
    global position, count

    if video_file is not None:
        success, image = video_file.read()
        if not success:
            print("Video playback ended.")
            return
    else:
        success, image = cap.read()
        if not success:
            print("Empty Camera")
            return

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    result = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    imlist = []

    if result.pose_landmarks:
        md_drawing.draw_landmarks(
            image, result.pose_landmarks, md_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=md_drawing_style.get_default_pose_landmarks_style()
        )
        for id, im in enumerate(result.pose_landmarks.landmark):
            h, w, _ = image.shape
            X, Y = int(im.x * w), int(im.y * h)
            imlist.append([id, X, Y])

    if len(imlist) != 0:
        if imlist[12][2] and imlist[11][2] >= imlist[14][2] and imlist[13][2]:
            position = "down"
        if imlist[12][2] and imlist[11][2] < imlist[14][2] and imlist[13][2] and position == "down":
            position = "up"
            count += 1
            print(count)
            # Calculate shoulder angles
            # shoulder_angle = calculate_angle(imlist[11][1], imlist[12][1], imlist[13][1])
            # print("Shoulder Angle:", shoulder_angle)

    frame = ImageTk.PhotoImage(Image.fromarray(image))
    video_label.config(image=frame)
    video_label.image = frame

    root.after(1, process_frame)

# Function to open the webcam for video capture

# # ...
def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    """
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = math.abs(math.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle

def open_webcam():
    global cap, video_file
    cap.release()
    video_file = None
    cap = cv2.VideoCapture(0)

# Function to open the video captured for detection of jumping jacks

def open_video():
    global cap, video_file
    cap.release()
    video_file = cv2.VideoCapture("Jumping Jacks.mkv")

# Function to open a video file for playback

button_frame = Frame(root)
button_frame.pack(pady=10)

# Creating a frame to hold the buttons

# webcam_button = Button(button_frame, text="Open WebCam", command=open_webcam)
# webcam_button.grid(row=0, column=0, padx=10)

# # Creating a button to open the webcam

# video_button = Button(button_frame, text="Open Video", command=open_video)
# video_button.grid(row=0, column=1, padx=10)

# Creating a button to open a video file

update_jump()
process_frame()

# Updating the jumping jack count and processing video frames

root.mainloop()

cap.release()
if video_file is not None:
    video_file.release()
cv2.destroyAllWindows()