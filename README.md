# Project Overview
This project aimed to use a machine learning model to provide a reliable fire and smoke detection system. The YOLOv8 algorithm detects fire and smoke in real time from a video stream. When either is detected, the system triggers sound alerts and sends email notifications with captured screenshots.



# Features
- **Real-time Detection:** The system utilizes a YOLOv8 model trained to detect fire and smoke in real-time via a connected camera.
  
- **Email Alerts:** When fire or smoke is detected, the system sends an automated email with a screenshot of the event.
  
- **Sound Notifications:** In addition to email alerts, the system plays an alert sound when fire or smoke is detected.
  
- **Customizable Confidence Thresholds:** The detection sensitivity for fire and smoke can be adjusted based on specific confidence thresholds to reduce false positives.
  
- **Screenshot Logging:** Screenshots of fire or smoke detections are saved automatically with a timestamp for logging purposes.



# Requirements
To run this project, you will need to install the following dependencies:

- **Python 3.12 or higher**
- **YOLOv8** (`pip install ultralytics`)
- **OpenCV** (`pip install opencv-python`)
- **PyGame** (`pip install pygame`)
- **smtplib** (Python's built-in email library, no installation needed)
- **EmailMessage** (from `email.message` module, built into Python)

You also need to download the trained model (`optimized150.pt`) and place it in the project directory.



# Installation
Follow these steps to set up and run the project:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/TalhaKarakoyunlu/Fire-and-Smoke-Detection.git
   cd Fire-and-Smoke-Detection

2. **Install the Dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Download YOLOv8 Model:** Make sure to place the latest trained model (optimized150.pt) in the project directory.

4. **Configure Email Credentials:** Replace `your_email` and `your_password` in the `send_email()` function.

5. **Prepare Alert Sound:** Ensure that the `alert_sound.mp3` file is in the project directory, you can also use an alert sound that you like.



# How to Run

1. **Run the YOLOv8 Live Detection Script:**
   ```bash
   python YOLOv8LiveCam.py

2. **Fire and Smoke Detection Logic:**
   - **Fire Detection:** If a fire is detected with confidence >0.55 for 2 seconds continuously, a screenshot is saved, an email is sent, and an alert sound plays.
   - **Smoke Detection:** If smoke is detected with confidence >0.75 for 3 seconds continuously, a screenshot is saved, an email is sent, and an alert sound plays.
   
3. **Exit:** Press the d key to exit the detection loop and close the webcam feed or use CTRL+C to keyboard interrupt.
  


# Customization

1. **Adjust Detection Thresholds:** You can modify the detection duration threshold for fire and smoke:

   ```bash
   detection_threshold_fire = 2  # Number of seconds fire must be detected
   detection_threshold_smoke = 3  # Number of seconds smoke must be detected

3. **Change Confidence Levels:** Modify the confidence thresholds for fire and smoke detection:
   
   ```bash
   if class_index == 0 and confidence > 0.55:  # Fire detection threshold
   if class_index == 1 and confidence > 0.75:  # Smoke detection threshold

# Troubleshooting

- **Video Source Error:** If there’s an error like "Error: Could not open video source," try changing the camera index in `cv2.VideoCapture()`:
  ```bash
  capture = cv2.VideoCapture(1)  # Change the index to 0 for your integral cam, 2 or 3 for other cameras

- **Email Issues:** Ensure your Gmail is properly configured for SMTP, using an App Password or enabling less secure app access.

- **Alert Sound Issues:** Ensure `alert_sound.mp3` is present in the project directory and pygame is correctly installed.

# Extra
- **YOLOv8.py** can be used to test the models on images and videos.

# License

This project is licensed under the MIT License.
