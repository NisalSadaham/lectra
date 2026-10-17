from google import genai
from dotenv import load_dotenv
from transcript_handling import load_transcript
import os
from pydantic import BaseModel
from assignment_storage import get_assignment
from assignment_storage import save_explanation

 

class Assignment(BaseModel):
    description:str
    requirements:list[str]
    min_word_count:int | None = None
    max_word_count:int | None = None
    deadline:str| None = None

class MultipleAssignments(BaseModel):
    list_assignments:list[Assignment]
class AssignmentExplanation(BaseModel):
    overview:str
    requirement_breakdown:list[str]
    action_plan:list[str]


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
transcript = load_transcript()

class TranscriptEmptyError(Exception):
    pass
class EmptyAssignmentError(Exception):
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

def explain_assignment(assignment):
    if assignment is None:
        raise EmptyAssignmentError("No assignment is there")
    description = assignment["description"]
    requirements = assignment["requirements"]
    prompt = f"""You are Lectra, an AI assistant that helps students understand assignments.
    Assignment description: {description}
    Requirements:{requirements}
    Provide:
    1. A simple overview of what the student must accomplish.
    2. A clear explanation of each requirement.
    3. An ordered, practical action plan.
    Use beginner-friendly language. Do not invent requirements or write the complete assignment for the student.
    Return the result using the AssignmentExplanation schema."""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
        "response_mime_type":"application/json",
        "response_schema":AssignmentExplanation,
        }
    )
    return response.parsed








