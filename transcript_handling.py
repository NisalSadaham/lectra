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

text1 = "Design a database for a small library."
text2 = "Design a database for a small library."
text3 = "Create a database for a small library."

print(generate_transcript_hash(text1) == generate_transcript_hash(text2))
print(generate_transcript_hash(text1) == generate_transcript_hash(text3))
     