from pydantic import BaseModel
from typing import Optional

class IncidentPayload(BaseModel):
    incident_sys_id: str
    number: str
    short_description: str
    description: Optional[str] = ""
    priority: int