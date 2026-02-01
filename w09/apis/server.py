from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Shot(BaseModel):
    number: int
    name: str
    sequence: str
    department: Optional[str] = None
    
shots = {
    1: {"id": 1, "name": "opening01", "sequence": "Intro", "department": "Cinematography"},
    2: {"id": 2, "name": "chase01", "sequence": "Action", "department": "Stunts"},
    3: {"id": 3, "name": "closing01", "sequence": "Outro", "department": "Editing"},
    4: {"id": 4, "name": "dialogue01", "sequence": "Drama", "department": "Sound"},
}

@app.get("/")
def index():
    return shots

@app.get("/shots/{shot_id}")
def get_shot_by_did(shot_id: int = Path(..., description="The ID of the shot to retrieve", gt=0)):
    return shots.get(shot_id, {"error": "Shot not found"})

@app.get("/shots/by-name/{shot_name}")
def get_shot_by_name(shot_name: str):
    for shot in shots.values():
        if shot["name"].lower() == shot_name.lower():
            return shot
    return {"error": "Shot not found"}

@app.post("/shots")
def create_shot(shot: Shot):
    new_id = max(shots.keys()) + 1
    shots[new_id] = {
        "id": new_id,
        "name": shot.name,
        "sequence": shot.sequence,
        "department": shot.department
    }
    return shots[new_id]

@app.put("/shots/{shot_id}")
def update_shot(shot_id: int, shot: Shot):
    if shot_id in shots:
        shots[shot_id].update({
            "name": shot.name,
            "sequence": shot.sequence,
            "department": shot.department
        })
        return shots[shot_id]
    return {"error": "Shot not found"}

@app.delete("/shots/{shot_id}")
def delete_shot(shot_id: int):
    if shot_id in shots:
        deleted_shot = shots.pop(shot_id)
        return {"message": "Shot deleted", "shot": deleted_shot}
    return {"error": "Shot not found"}