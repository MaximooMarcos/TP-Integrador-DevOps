from fastapi import APIRouter, HTTPException, status
from app.database import incidents_db
from app.models import Incident

router = APIRouter(prefix="/incidents", tags=["Incidentes IT"])


@router.get("", status_code=status.HTTP_200_OK)
def get_incidents():
    return incidents_db


@router.get("/{incident_id}", status_code=status.HTTP_200_OK)
def get_incident(incident_id: int):
    for incident in incidents_db:
        if incident["id"] == incident_id:
            return incident
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Incidente no encontrado"
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_incident(incident: Incident):
    new_id = max([i["id"] for i in incidents_db], default=0) + 1
    new_incident = incident.model_dump()
    new_incident["id"] = new_id
    incidents_db.append(new_incident)
    return new_incident

@router.put("/{incident_id}", status_code=status.HTTP_200_OK)
def update_incident(incident_id: int, updated_incident: Incident):
    for idx, incident in enumerate(incidents_db):
        if incident["id"] == incident_id:
            updated_data = updated_incident.model_dump()
            updated_data["id"] = incident_id
            incidents_db[idx] = updated_data
            return updated_data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Incidente no encontrado"
    )

@router.delete("/{incident_id}", status_code=status.HTTP_200_OK)
def delete_incident(incident_id: int):
    for idx, incident in enumerate(incidents_db):
        if incident["id"] == incident_id:
            removed = incidents_db.pop(idx)
            return {
                "message": f"Incidente {incident_id} eliminado",
                "incident": removed,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Incidente no encontrado"
    )