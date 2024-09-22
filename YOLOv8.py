from ultralytics import YOLO
import cv2


# # For testing the model on an image
model = YOLO("optimized150.pt")
model.predict(source="test_pics/mumlar2.png", imgsz=640, conf=0.5, save=True)



# # For testing the model on a video
# # Load the model
# model = YOLO("optimized150.pt")  # Best model selected from different epochs
# capture = cv2.VideoCapture("test_videos/smoke.mp4")  # Adjust the path if using a different video source

# if not capture.isOpened():
#     print("Error: Could not open video source.")
#     exit()

# # Set delay in milliseconds (increase to slow down the video)
# delay = 2  # Increase this value to slow down to match the fps (e.g., try 50 for slower)

# while True:
#     isTrue, frame = capture.read()
#     # Check if the frame was successfully captured
#     if isTrue:
#         # Perform inference on the frame
#         results = model.predict(source=frame, imgsz=640, conf=0.5, show=False)  # Disable show to prevent extra window

#         # Filter detections based on confidence thresholds for fire and smoke
#         detections = results[0].boxes
#         filtered_boxes = []

#         for box in detections:
#             class_index = int(box.cls)
#             confidence = box.conf

#             if class_index == 0 and confidence > 0.55:  # Fire detected with confidence > 0.55
#                 filtered_boxes.append(box)  # Add to filtered boxes for plotting
#             elif class_index == 1 and confidence > 0.75:  # Smoke detected with confidence > 0.75
#                 filtered_boxes.append(box)  # Add to filtered boxes for plotting

#         # Update the results with filtered boxes
#         results[0].boxes = filtered_boxes
        
#         # Draw the results on the frame
#         annotated_frame = results[0].plot()  # Plot the results on the frame

#         # Display the frame with detections
#         cv2.imshow('YOLOv8 Detection', annotated_frame)

#         # Break the loop if 'd' key is pressed
#         if cv2.waitKey(delay) & 0xFF == ord('d'):  # Increase delay to slow down the video
#             break
#     else:
#         # If the frame could not be read, break the loop
#         break

# # Release the capture and close the window
# capture.release()
# cv2.destroyAllWindows()
