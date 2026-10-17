import hashlib

def save_transcript(extracted_text):
    with open("assignment_transcript.txt",'w') as file:
        file.write(extracted_text)

def load_transcript():
    transcript = ""
    try:
        with open("assignment_transcript.txt",'r') as file:
                file_data = file.readlines()
                for data in file_data:
                     transcript += data.strip("")
                return transcript if len(transcript) > 0 else  None        
    except FileNotFoundError:
        print("File not found")

def generate_transcript_hash(transcript):
    hashed_transcript = hashlib.sha256(transcript.encode('utf-8')).hexdigest()
    return hashed_transcript

