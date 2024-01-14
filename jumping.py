import time
import cv2
from tkinter import *
from tkinter import simpledialog
from PIL import Image, ImageTk
import mediapipe as md

# Mutable object to control the loop
running = [True]

def stop_execution_internal():
    running[0] = False

def get_username():
    username = simpledialog.askstring("Input", "Enter your username:")
    return username

def run_jumping_jack_app():
    md_drawing = md.solutions.drawing_utils
    md_drawing_style = md.solutions.drawing_styles
    md_pose = md.solutions.pose

    count = 0
    position = None
    start_time = time.time()  # Record the start time
    username = get_username()  # Get username here

    cap = cv2.VideoCapture(0)
    video_file = None

    root = Tk()
    root.title("JUMPING JACK")

    # Set the window size to cover the whole screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')

    root.configure(bg="#FFD700")

    f1 = LabelFrame(root, bg="#0000FF")
    f1.place(relx=0.5, rely=0.5)  # This is vid background
    label = Label(root, text="Jumping Jacks in Progress", font=("Arial", 24))
    label.pack(pady=10)

    timer_label = Label(root, text=f"Time Remaining: 60 seconds", font=("Arial", 18), fg="red")
    timer_label.pack(pady=10)

    video_label = Label(root)
    video_label.pack(fill=BOTH, expand=YES)  # Adjust the video_label size to fill the window

    def close():
        root.destroy()

    Button(f1, text="Exit the Application", bg='#fffdd0', fg='red', font=("Calibri", 14, "bold"), command=close).place(
        relx=0.11, rely=0.8, anchor="center")

    pose = md_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.7
    )

    def update_jump():
        nonlocal count
        label.config(text=f"Jumping Jacks Count: {count}")
        elapsed_time = time.time() - start_time

        # Check if the duration is not exceeded
        if elapsed_time < 20:  # Set the duration to 20 seconds
            # Update the countdown every second
            duration_remaining = int(20 - elapsed_time)
            timer_label.config(text=f"Time Remaining: {duration_remaining} seconds")
            label.after(1000, update_jump)
        else:
            save_user_info(username, count)  # Save user information
            show_congratulations(root)


    def process_frame():
        nonlocal position, count

        if not running[0]:
            return

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

        frame = ImageTk.PhotoImage(Image.fromarray(image))
        video_label.config(image=frame)
        video_label.image = frame

        if running[0]:
            root.after(1, process_frame)

    def open_webcam():
        nonlocal cap, video_file
        cap.release()
        video_file = None
        cap = cv2.VideoCapture(0)

    def open_video():
        nonlocal cap, video_file
        cap.release()
        video_file = cv2.VideoCapture("Jumping Jacks.mkv")

    # Adding a button to stop the execution
    stop_button = Button(f1, text="Stop Execution", bg='#fffdd0', fg='red',
                         font=("Calibri", 14, "bold"), command=stop_execution_internal)
    stop_button.place(relx=0.3, rely=0.8, anchor="center")

    button_frame = Frame(root)
    button_frame.pack(pady=10)

    update_jump()
    process_frame()

    root.mainloop()

    cap.release()
    cv2.destroyAllWindows()

def save_user_info(username, count):
    with open("user_info.txt", "a") as file:
        file.write(f"Username: {username}, Jumping Jacks Count: {count}\n")

def show_congratulations(root):
    # Display congratulations message and image
    congrats_label = Label(root, text="Congratulations! You have completed your Jumping Jacks!", font=("Arial", 24), fg="Purple")
    congrats_label.place(relx=0.5, rely=0.4, anchor="center")

    dino_image = Image.open("dino.png")
    dino_image = dino_image.resize((200, 200), Image.ANTIALIAS)
    dino_image = ImageTk.PhotoImage(dino_image)

    dino_label = Label(root, image=dino_image)
    dino_label.image = dino_image
    dino_label.place(relx=0.5, rely=0.6, anchor="center")

    # After a delay, close the application
    root.after(3000, root.destroy)


if __name__ == '__main__':
    # Get username before running the main app
    username = get_username()

    # Run the main app with the provided username
    run_jumping_jack_app(username)
