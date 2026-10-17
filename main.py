from fastapi import FastAPI
from fastapi import HTTPException
from assignment_storage import get_assignment,save_assignment,assigment_exists
from assignment_service import coordination
from pydantic import BaseModel
from ai_processor import extract_assignment

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript:str


@app.get('/assignments')
def get_assigment_data():
    assignments = get_assignment()
    return{
        "response":assignments
    }
@app.post('/assignments/{assignment_id}/explanation')
def get_explanation(assignment_id:int):
    explanation = coordination(assignment_id=assignment_id)
    if explanation is None:
        raise HTTPException(status_code=404,detail="file not found")
    return{
        "explanation":explanation
    }
@app.post('/assignment/import')
def transcript_request(transcript_request:TranscriptRequest):
    saved_assignments = []
    duplicate_assignments = []
    if transcript_request.transcript.strip() == "":
        raise HTTPException(status_code=400,detail="Bad request(Transcript cannot be empty)")
    extracted_assignment = extract_assignment(transcript_request.transcript)
    for assignment in extracted_assignment.list_assignments:
        duplicate = assigment_exists()
        if not duplicate:
            save_assignment(assignment=assignment)
            saved_assignments.append(assignment)
        else:
            duplicate_assignments.append(assignment)
    return{
        "saved_assigments":saved_assignments,
        "duplicate_assigments":duplicate_assignments
    }
    
