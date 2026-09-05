import os
import requests
import base64 # Added this library
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

SN_INSTANCE_URL = os.getenv("SN_INSTANCE_URL")
SN_USERNAME = os.getenv("SN_USERNAME")
SN_PASSWORD = os.getenv("SN_PASSWORD")
class ServiceNowUpdatePayload(BaseModel):
    state: Optional[int] = None 
    close_notes: Optional[str] = None
    close_code: Optional[str] = None
    work_notes: Optional[str] = None
    comments: Optional[str] = None

def update_servicenow_ticket(incident_sys_id: str, ai_result: dict):
    url = f"{SN_INSTANCE_URL}/api/now/table/incident/{incident_sys_id}?sysparm_input_display_value=true"
    
    decision = ai_result.get("decision")
    message = ai_result.get("message")
    
    if decision == "respond":
        update_data = ServiceNowUpdatePayload(
            state=6, 
            close_notes=message, 
            close_code="Solution provided", 
            work_notes=message  
        )
    elif decision == "ask":
        update_data = ServiceNowUpdatePayload(comments=message)
    elif decision == "escalate":
        update_data = ServiceNowUpdatePayload(work_notes=f"Escalation Reason: {message}")
    else:
        return

    payload = update_data.model_dump(exclude_unset=True)

    # Prepare manual base64 encoding for the password
    auth_string = f"{SN_USERNAME}:{SN_PASSWORD}"
    encoded_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    # Add the Authorization header manually
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_auth}" 
    }
    
    try:
        # Removed auth=(SN_USERNAME, SN_PASSWORD) to rely on headers
        response = requests.patch(
            url, 
            json=payload, 
            headers=headers
        )
        
        print(f"HTTP Status: {response.status_code}")
        print(f"ServiceNow Response: {response.text}")
        response.raise_for_status() 
        print(f"Successfully updated ticket {incident_sys_id} in ServiceNow.")
        
    except Exception as e:
        print(f"Failed to update ServiceNow ticket: {e}")