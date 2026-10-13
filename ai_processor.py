from google import genai
from dotenv import load_dotenv
from transcript_handling import load_transcript
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
transcript = load_transcript()

class TranscriptEmptyError(Exception):
    pass

def generate_summary(transcript):
    if transcript is None:
        raise TranscriptEmptyError("Transcript is empty")
    
    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=f"Summarize {transcript} concisely, covering all key points. Use only transcript content. Output only the summary."
    )
    return response.text

try:
    gemini_summary = generate_summary()
    print(gemini_summary)
except TranscriptEmptyError as e:
    print(e)
except Exception as e:
    print(e)









