from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import cv2

# Load config from a config file
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file('COCO-Detection/retinanet_R_101_FPN_3x.yaml'))
cfg.MODEL.WEIGHTS = 'C:\Archive\Study\Deep_learning\model_0003999.pth'
cfg.MODEL.DEVICE = 'cpu'

# Create predictor instance
predictor = DefaultPredictor(cfg)

# Load image
image = cv2.imread(r"C:\Archive\Study\Deep_learning\00004.jpg")

# Perform prediction
outputs = predictor(image)

threshold = 0.5

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
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Add text with class number and background
        class_label = classes[pred]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        font_color = (255, 255, 255)  # White color for text
        background_color = color  # Background color matches the rectangle color

        text_size = cv2.getTextSize(class_label, font, font_scale, font_thickness)[0]
        cv2.rectangle(image, (x1, y1 - 10 - text_size[1]), (x1 + text_size[0], y1 - 10), background_color, -1)
        cv2.putText(image, class_label, (x1, y1 - 10), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

cv2.imshow('image', image)
cv2.waitKey(0)
