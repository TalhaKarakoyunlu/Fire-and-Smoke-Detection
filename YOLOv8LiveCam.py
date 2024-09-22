from ultralytics import YOLO
import cv2
import pygame
import time
import os
import smtplib
from email.message import EmailMessage

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Email sending function
def send_email(to_email, subject, body, screenshot_path):
    your_email = "YOUR_GMAIL_HERE"
    your_password = "YOUR_APP_PASSWORD_HERE"  # App password
    
    # Create the email content
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = your_email
    msg['To'] = to_email

    # Attach the screenshot
    with open(screenshot_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(screenshot_path)
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)

    # Establish a connection to the Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(your_email, your_password)
        smtp.send_message(msg)

    print(f"Email sent successfully to {to_email} with screenshot: {screenshot_path}")

# Play the alert sound
def play_alert_sound():
    pygame.mixer.music.load('alert_sound.mp3')  # Ensure you have an alert sound file named 'alert_sound.mp3'
    pygame.mixer.music.play()

# Model setup
model = YOLO("optimized150.pt")  # Best model selected from different epochs
capture = cv2.VideoCapture(1)  # Adjust the index if using a different camera

if not capture.isOpened():
    print("Error: Could not open video source.")
    exit()

detection_duration_fire = 0
detection_duration_smoke = 0
detection_threshold_fire = 2  # Fire detected for 2 seconds
detection_threshold_smoke = 3  # Stricter threshold for smoke detection
alert_sent_fire = False
alert_sent_smoke = False

while True:
    isTrue, frame = capture.read()
    if isTrue:
        # Perform inference on the frame
        results = model.predict(source=frame, imgsz=640, conf=0.5, show=False)
        
        # Filter detections based on confidence thresholds for fire and smoke
        detections = results[0].boxes
        fire_detected = False
        smoke_detected = False
        
        # Filter out boxes with confidence less than threshold
        filtered_boxes = []
        
        for box in detections:
            class_index = int(box.cls)
            confidence = box.conf

            if class_index == 0 and confidence > 0.55:  # Fire detected with confidence > 0.5
                fire_detected = True
                filtered_boxes.append(box)  # Add to filtered boxes for plotting
            elif class_index == 1 and confidence > 0.75:  # Stricter threshold for smoke detection
                smoke_detected = True
                filtered_boxes.append(box)  # Add to filtered boxes for plotting

        # Update duration for fire detection
        if fire_detected:
            detection_duration_fire += 1 / 30  # Assuming ~30 FPS
        else:
            detection_duration_fire = 0  # Reset fire detection duration if not detected

        # Update duration for smoke detection
        if smoke_detected:
            detection_duration_smoke += 1 / 30  # Assuming ~30 FPS
        else:
            detection_duration_smoke = 0  # Reset smoke detection duration if not detected

        # Fire alert if detected for the threshold time
        if detection_duration_fire >= detection_threshold_fire and not alert_sent_fire:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = f"./fire_detected_{timestamp}.jpg"  # Save to root directory
            
            # Save the filtered frame (with only high-confidence boxes)
            results[0].boxes = filtered_boxes  # Only plot filtered boxes
            annotated_frame = results[0].plot()
            cv2.imwrite(screenshot_path, annotated_frame)

            # Play alert sound and send email
            play_alert_sound()
            email_body = "Fire has been detected. See the attached screenshot."
            send_email("YOUR_GMAIL@gmail.com", "Fire Detected!", email_body, screenshot_path)

            alert_sent_fire = True  # Ensure alert is only sent once per event
            print(f"Fire screenshot saved and alert triggered: {screenshot_path}")
        
        # Smoke alert if detected for the threshold time
        if detection_duration_smoke >= detection_threshold_smoke and not alert_sent_smoke:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = f"./smoke_detected_{timestamp}.jpg"  # Save to root directory
            
            # Save the filtered frame (with only high-confidence boxes)
            results[0].boxes = filtered_boxes  # Only plot filtered boxes
            annotated_frame = results[0].plot()
            cv2.imwrite(screenshot_path, annotated_frame)

            # Play alert sound and send email
            play_alert_sound()
            email_body = "Smoke has been detected. See the attached screenshot."
            send_email("YOUR_GMAIL@gmail.com", "Smoke Detected!", email_body, screenshot_path)

            alert_sent_smoke = True  # Ensure alert is only sent once per event
            print(f"Smoke screenshot saved and alert triggered: {screenshot_path}")
        
        # Reset the alert if detection stops before threshold
        if detection_duration_fire < detection_threshold_fire:
            alert_sent_fire = False
        if detection_duration_smoke < detection_threshold_smoke:
            alert_sent_smoke = False

        # Show the annotated frame in the video window
        results[0].boxes = filtered_boxes  # Only show filtered boxes
        annotated_frame = results[0].plot()
        cv2.imshow('YOLOv8 Webcam', annotated_frame)

        # Break the loop if 'd' key is pressed
        if cv2.waitKey(5) & 0xFF == ord('d'):
            break
    else:
        break

# Release the capture and close the window
capture.release()
cv2.destroyAllWindows()
