from __future__ import annotations

import io
import logging
from pathlib import Path

from PIL import Image
from fastapi import UploadFile
from ultralytics import YOLO

from core.settings import settings
from schemas.models import ModelBoxesResponseItemsSchema, ModelBoxesResponseSchema

logger = logging.getLogger("API")


class ModelService:
    def __init__(self):
        self.model_loaded = False
        self.model: YOLO | None = None
        self._load_model()

    def _load_model(self):
        try:
            path = Path(settings.MODEL_PATH)
            if not path.exists():
                raise FileNotFoundError

            self.model = YOLO(path)

            self.model_loaded = True
        except Exception as e:
            logger.error("model loading error", exc_info=e)

    def detect_by_image(self, image: UploadFile) -> ModelBoxesResponseItemsSchema:
        img = Image.open(io.BytesIO(image.file.read()))
        model_response = self.model.predict(img)[0]
        boxes = model_response.boxes

        names = self.model.names

        items = []
        for cls, xywhn, xywh, xyxy, xyxyn in zip(boxes.cls, boxes.xywhn, boxes.xywh, boxes.xyxy, boxes.xyxyn):
            items.append(
                ModelBoxesResponseSchema(
                    cls=names[int(cls)],
                    xywhn=xywhn.tolist(),
                    xywh=xywh.tolist(),
                    xyxy=xyxy.tolist(),
                    xyxyn=xyxyn.tolist(),
                )
            )

        return ModelBoxesResponseItemsSchema(items=items)
