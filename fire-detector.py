import cv2
import numpy as np
from twilio.rest import Client
import playsound
import threading

Alarm_Status = False
Fire_Reported = 0
terminate_alarm = False 
fire_detected = False  # Variable to track fire detection status
sms_sent = False 


 # Add the phone numbers you want to send the SOS to

def play_alarm_sound_function():
    while not terminate_alarm and fire_detected:
        playsound.playsound('alarm-sound.mp3', True)

def send_sos_sms():
    global sms_sent 
    TWILIO_SID = "AC6290f37eb02e394cebd0a2e4b14469ec"
    TWILIO_AUTH_TOKEN = "190019cb543a1dd292b6608d9b43b4bf"
    try:
        if not sms_sent: 
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                body="Warning: A fire accident has been reported on ABC Company",
                from_ = '+16506677927',
                to = '+918178621941'
            )

            print(f"SMS sent to SID: {message.sid}")
            sms_sent = True

    except Exception as e:
        print(f"Error sending SMS: {e}")

video = cv2.VideoCapture("video.mp4")  # If you want to use webcam, use Index like 0,1.

while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 15000:
        Fire_Reported += 1
        fire_detected = True
    else:
        Fire_Reported = 0
        fire_detected = False

    cv2.imshow("output", frame)

    if Fire_Reported >= 1:

        if not Alarm_Status:
            alarm_thread = threading.Thread(target=play_alarm_sound_function)
            alarm_thread.start()
            Alarm_Status = True

        # Send SOS SMS
        if not fire_detected:
            threading.Thread(target=send_sos_sms).start()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
terminate_alarm = True
alarm_thread.join()
