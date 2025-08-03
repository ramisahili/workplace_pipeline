from pydantic import BaseModel

class TransformRequest(BaseModel):
    start_date: str  # "2025-01-01"
    end_date: str    # "2025-01-31"
