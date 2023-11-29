from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import cv2

# Load configuration
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file('COыCO-Detection/retinanet_R_101_FPN_3x.yaml'))
cfg.MODEL.WEIGHTS = 'C:\Archive\Study\Deep_learning\program\output\model_0003999.pth'
cfg.MODEL.DEVICE = 'cpu'
predictor = DefaultPredictor(cfg)

# Open video capture
video_path = r'C:\Archive\Study\Deep_learning\yolo_data\traffic-sign-to-test.mp4'  # Specify the path to your video file
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties
width = int(cap.get(3))
height = int(cap.get(4))
fps = cap.get(5)

# Create VideoWriter object to save the output video
out_path = 'output_video.avi'
out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

# Process each frame
frame_count = 0
while True:
    ret, frame = cap.read()

    # Break the loop if the video is over
    if not ret:
        break

    frame_count += 1

    # Perform prediction for every 10th frame
    if frame_count % 1 == 0:
        # Perform prediction
        outputs = predictor(frame)

        threshold = 0.6

        # Display predictions
        preds = outputs["instances"].pred_classes.tolist()
        scores = outputs["instances"].scores.tolist()
        bboxes = outputs["instances"].pred_boxes

        for j, bbox in enumerate(bboxes):
            bbox = bbox.tolist()

            score = scores[j]
            pred = preds[j]

            classes = ["prohibitory", "danger", "mandatory", "other"]

            if score > threshold:
                x1, y1, x2, y2 = [int(i) for i in bbox]

                # Determine color based on class
                if classes[pred] == "prohibitory":
                    color = (128, 0, 128)  # Purple
                elif classes[pred] == "danger":
                    color = (0, 0, 255)  # Red
                elif classes[pred] == "mandatory":
                    color = (0, 255, 0)  # Green
                elif classes[pred] == "other":
                    color = (255, 0, 0)  # Blue

                # Draw rectangle with class-specific color
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Add text with class number and background
                class_label = classes[pred]
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.2
                font_thickness = 2
                font_color = (255, 255, 255)  # White color for text
                background_color = color  # Background color matches the rectangle color

                text_size = cv2.getTextSize(class_label, font, font_scale, font_thickness)[0]
                cv2.rectangle(frame, (x1, y1 - 10 - text_size[1]), (x1 + text_size[0], y1 - 10), background_color, -1)
                cv2.putText(frame, class_label, (x1, y1 - 10), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    # Save the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Video', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and writer objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
