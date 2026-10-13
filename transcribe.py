from faster_whisper import WhisperModel
from transcript_handling import save_transcript

model = WhisperModel(model_size_or_path="base",device="cpu",compute_type="int8")

segments,info = model.transcribe("./sample_recording/sample.m4a")
print(info.duration)
print(info.language)

print("Starting transcription output...")
extracted_text = ""
for segment in segments:
    extracted_text += f"{segment.text}" + "\n" 

save_transcript(extracted_text=extracted_text)
print("Trasncript saved successfully..")

