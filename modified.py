import whisper
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import shutil

# Initialize the FastAPI app
app = FastAPI()

# Load the Whisper model on the CPU
model = whisper.load_model("base", device='cpu')

# Define the endpoint for file upload and transcription
@app.post("/transcribe/")
async def transcribe_file(file: UploadFile = File(...)):
    # Determine file type and handle appropriately
    supported_extensions = {".mp4", ".wav", ".mp3", ".m4a", ".flac", ".ogg"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in supported_extensions:
        return {"error": f"Unsupported file format: {file_extension}. Please upload one of {supported_extensions}."}

    # Step 1: Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 2: Load the audio (whether from video or audio file)
    try:
        audio = whisper.load_audio(temp_path)
        # Transcribe the audio
        result = model.transcribe(audio)
        transcription = result["text"]

        # Save the transcription to a text file
        output_file_path = f"{Path(file.filename).stem}_transcription.txt"
        with open(output_file_path, "w") as transcription_file:
            transcription_file.write(transcription)

        # Clean up the temporary file
        Path(temp_path).unlink()

        return {
            "filename": file.filename,
            "transcription": transcription,
            "output_file": output_file_path,
        }

    except Exception as e:
        return {"error": str(e)}

