# Fire Detection System in Python

## Overview

This project implements a fire detection system using Python, OpenCV, and Twilio. The system analyzes video frames to detect the presence of fire and sends an SOS SMS using Twilio if a fire is detected.

## Features

- Real-time fire detection in video streams or files.
- Alarm activation when fire is detected.
- Automated SOS SMS alert using Twilio.

## Prerequisites

Make sure you have the following installed on your system:

- Python (>=3.6)
- OpenCV
- Twilio Python library (twilio)
- playsound
- numpy
- pandas

```bash
pip install opencv-python numpy twilio playsound==1.2.2
```

## Configuration

Replace the placeholder values in the code:

- `TWILIO_SID`: Your Twilio account SID.
- `TWILIO_AUTH_TOKEN`: Your Twilio authentication token.
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number.
- `TO_PHONE_NUMBERS`: List of phone numbers to receive SOS SMS.

Add your Twilio credentials and phone numbers in the code:

```python
TWILIO_SID = "Your_Twilio_SID"
TWILIO_AUTH_TOKEN = "Your_Twilio_Authentication_Token"
TWILIO_PHONE_NUMBER = "Your_Twilio_Phone_Number"
TO_PHONE_NUMBERS = ["Recipient_Phone_Number_1", "Recipient_Phone_Number_2"]

```

## Usage

Run the Python script:

```bash
python fire_detection_system.py
```

## Important Notes

- Ensure proper video input: The system supports video files (e.g., .mp4), and you can modify the code for webcam input.

## License

This project is licensed under the MIT License.

## Acknowledgments

- OpenCV: [https://opencv.org/](https://opencv.org/)
- Twilio: [https://www.twilio.com/](https://www.twilio.com/)

Feel free to contribute or report issues!





