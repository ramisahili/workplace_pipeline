from fastapi import APIRouter
from .models.request_model import TransformRequest
from .services.transformer_service import run_transformation

router = APIRouter()

@router.post("/transform")
def run_transform(request: TransformRequest):
    documents_count = run_transformation(request.start_date, request.end_date)
    return {"message": f"Transformation complete, processed {documents_count} documents"}
