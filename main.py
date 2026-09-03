from fastapi import FastAPI, BackgroundTasks, status
from models import IncidentPayload
from ai_service import analyze_incident
from servicenow_client import update_servicenow_ticket
import uvicorn

app = FastAPI()

# In-memory set
processed_incidents = set()

def process_incident_background(incident: IncidentPayload):
    print(f"Processing in background: {incident.number}")

    try:
        ai_result = analyze_incident(incident)
        print(f"AI Decision: {ai_result}")
        
        update_servicenow_ticket(incident.incident_sys_id, ai_result)
        
    except Exception as e:
        print(f"Error processing incident {incident.number}: {e}")

@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(incident: IncidentPayload, background_tasks: BackgroundTasks):
    if incident.incident_sys_id in processed_incidents:
        return {"message": "Incident already processed."}
    
    processed_incidents.add(incident.incident_sys_id)
    
    background_tasks.add_task(process_incident_background, incident)
    
    return {"message": "Incident accepted for processing."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)