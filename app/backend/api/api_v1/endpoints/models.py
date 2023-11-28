from fastapi import APIRouter, UploadFile
from fastapi.requests import Request

from schemas.models import ModelBoxesResponseItemsSchema
from services.model import ModelService

router = APIRouter()


@router.post("/:image", response_model=ModelBoxesResponseItemsSchema)
async def detect_by_image(request: Request, file: UploadFile):
    service: ModelService = request.app.state.model_service
    return service.detect_by_image(file)
