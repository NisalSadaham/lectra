from fastapi import FastAPI
from fastapi import HTTPException
from assignment_storage import get_assignment,save_assignment,assigment_exists,save_transcript_import,find_transcript_import,get_assignments_by_import_id,find_completed_transcript_import,delete_transcript_import
from assignment_service import coordination
from pydantic import BaseModel
from ai_processor import extract_assignment
from transcript_handling import generate_transcript_hash
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:54169"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    transcript:str
    duplicate_action: Literal["reuse", "import_again"] | None = None


@app.get('/assignments')
def get_assignment_data():
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
    status = "completed"
    message = "Assignments imported successfully."
    if transcript_request.transcript.strip() == "":
        raise HTTPException(status_code=400,detail="Bad request(Transcript cannot be empty)")
    transcript_hash = generate_transcript_hash(transcript_request.transcript)
    existing_import = find_completed_transcript_import(transcript_hash)
    if transcript_request.duplicate_action == None and existing_import is not None:
        raise HTTPException(status_code=400,detail="bad request:Choose whether to reuse or import again")
    if existing_import is not None and transcript_request.duplicate_action == "reuse":
        import_id = existing_import[0]
        assignments = get_assignments_by_import_id(import_id)
        return {
        "status":status,
        "message": "Import completed, existing assignments reused successfully.",
        "assignments": assignments
        }
    else:
        import_id = save_transcript_import(transcript_hash=transcript_hash)
    try:
        extracted_assignment = extract_assignment(transcript_request.transcript)
    except Exception:
        delete_transcript_import(import_id=import_id)
        raise HTTPException(status_code=500,detail="Failed to process transcript. Please try again")
   

    for assignment in extracted_assignment.list_assignments:
        duplicate = assigment_exists(assignment.description)
        if not duplicate:
            save_assignment(assignment=assignment,import_id=import_id)
            saved_assignments.append(assignment)
        else:
            duplicate_assignments.append(assignment)
    if len(extracted_assignment.list_assignments) == 0:
        message = "The import completed, but no assignments were found in the transcript."
    elif not saved_assignments:
            message = "Import completed, but no new assignments were saved."
    return{
        "status":status,
        "message":message,
        "saved_assignments":saved_assignments,
        "duplicate_assignments":duplicate_assignments
    }
    
