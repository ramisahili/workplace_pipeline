from pydantic import BaseModel, Field
from typing import Optional

class DocumentModel(BaseModel):
    body_id: Optional[str] = None
    body_name: Optional[str] = None
    page: Optional[int] = 0
    ref_no: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    partition_date: Optional[str] = None
    file_path: Optional[str] = None
    file_hash: Optional[str] = None
    file_name: Optional[str] = None
