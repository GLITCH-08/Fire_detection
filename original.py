import cv2
import numpy as np
import imutils
from twilio.rest import Client
import playsound
import threading
from imutils.object_detection import non_max_suppression

# Initialize global variables
Alarm_Status = False
Fire_Reported = 0
terminate_alarm = False
fire_detected = False
sms_sent = False

# Load the pre-trained HOG detector for pedestrian detection
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Function to detect people in a frame
def detect_people(frame):
    # Detect people using HOG
    rects, _ = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)

    # Apply non-maxima suppression to suppress overlapping boxes
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    
    # Count the number of people detected
    count = len(pick)

    # Draw bounding boxes around detected people
    for x, y, w, h in pick:
        cv2.rectangle(frame, (x, y), (w, h), (139, 34, 104), 2)

    return frame, count

# Function to play alarm sound
def play_alarm_sound_function():
    while not terminate_alarm and fire_detected:
        playsound.playsound('alarm-sound.mp3', True)

# Function to send SOS SMS
def send_sos_sms():
    global sms_sent
    TWILIO_SID = "Your_TWILIO_SID"
    TWILIO_AUTH_TOKEN = "Your_TWILIO_AUTH_TOKEN"
    
    # Add your Twilio account SID and authentication token
    try:
        if not sms_sent:
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                body="Warning: A fire accident has been reported!",
                from_='+16506677927',  # Your Twilio phone number
                to='+918178621941'  # Recipient's phone number
            )

            print(f"SMS sent to SID: {message.sid}")
            sms_sent = True

    except Exception as e:
        print(f"Error sending SMS: {e}")

# Load video or webcam feed
video = cv2.VideoCapture('180301_06_B_CityRoam_01.mp4')  # Replace "video.mp4" with 0 for webcam

# Initialize alarm_thread variable
alarm_thread = None  

while True:
    # Read frame from video feed
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    # Resize frame for better performance
    frame = cv2.resize(frame, (540, 380))

    # Blur frame and convert to HSV color space
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for fire detection in HSV color space
    lower = np.array([0, 120, 70])
    upper = np.array([10, 255, 255])
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # Create a mask for fire detection
    mask = cv2.inRange(hsv, lower, upper)

    # Perform bitwise AND operation to get regions with fire color
    output = cv2.bitwise_and(frame, hsv, mask=mask)

    # Count non-zero pixels in the mask
    no_red = cv2.countNonZero(mask)

    # Check if fire is detected
    if int(no_red) > 3000:
        Fire_Reported += 1
        fire_detected = True
    else:
        Fire_Reported = 0
        fire_detected = False

    # Display fire detection status on frame
    cv2.putText(frame, "Fire Detected" if fire_detected else "No Fire", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Detect people in the frame and count them
    frame, people_count = detect_people(frame)
    
    # Display people count on frame
    cv2.putText(frame, f"People Count: {people_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Combine frames horizontally for display
    combined_frame = np.hstack((frame, output))

    # Display combined frame
    cv2.imshow("Fire and People Detection", combined_frame)

    # Perform actions if fire is reported
    if Fire_Reported >= 1:
        if not Alarm_Status:
            alarm_thread = threading.Thread(target=play_alarm_sound_function)
            alarm_thread.start()
            Alarm_Status = True

        # Send SOS SMS
        if not fire_detected:
            threading.Thread(target=send_sos_sms).start()

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video feed and close all windows
cv2.destroyAllWindows()
video.release()

# Join the alarm thread outside the loop
if alarm_thread is not None:
    terminate_alarm = True
    alarm_thread.join()
