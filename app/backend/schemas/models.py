from pydantic import BaseModel, Field


class ModelBoxesResponseSchema(BaseModel):
    cls: str
    xywhn: list[float] = Field(..., min_items=4, max_items=4)
    xywh: list[float] = Field(..., min_items=4, max_items=4)
    xyxy: list[float] = Field(..., min_items=4, max_items=4)
    xyxyn: list[float] = Field(..., min_items=4, max_items=4)


class ModelBoxesResponseItemsSchema(BaseModel):
    items: list[ModelBoxesResponseSchema]
