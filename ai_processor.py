from google import genai
from dotenv import load_dotenv
from transcript_handling import load_transcript
import os
from pydantic import BaseModel
import json
 

class Assignment(BaseModel):
    description:str
    requirements:list[str]
    min_word_count:int | None = None
    max_word_count:int | None = None
    deadline:str| None = None

class MultipleAssignments(BaseModel):
    list_assigments:list[Assignment]


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
transcript = load_transcript()

class TranscriptEmptyError(Exception):
    pass

def extract_assignment(transcript):
    if transcript is None:
        raise TranscriptEmptyError("Transcript is empty")
    
    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=f"Read the transcript {transcript} and extract every assignment mentioned. Return each assignment separately. Include its description, all requirements, minimum and maximum word counts, and deadline. Only use information explicitly stated in the transcript. Preserve word-count ranges exactly; do not calculate or guess values. If an optional field is missing, return None. Do not invent information",
    config={
        "response_mime_type": "application/json",
        "response_schema":MultipleAssignments,
    }
        
    )
  
    return response.parsed

try:
    extracted_assignments = extract_assignment(transcript=transcript)
    for assignment in extracted_assignments.list_assigments:
        print(assignment.description)
        print(assignment.requirements)
        print(assignment.min_word_count)
        print(assignment.max_word_count)
        print(assignment.deadline)
except TranscriptEmptyError as e:
    print(e)
except Exception as e:
    print(e)









