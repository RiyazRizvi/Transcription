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
async def transcribe_video(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        video_path = f"temp_{file.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load and transcribe the audio from the video file
        audio = whisper.load_audio(video_path)
        result = model.transcribe(audio)
        transcription = result["text"]

        # Save transcription to a text file
        output_file_path = f"{Path(file.filename).stem}_transcription.txt"
        with open(output_file_path, "w") as transcription_file:
            transcription_file.write(transcription)

        # Clean up the uploaded video file
        Path(video_path).unlink()

        # Return the transcription as response
        return {
            "filename": file.filename,
            "transcription": transcription,
            "output_file": output_file_path
        }

    except Exception as e:
        return {"error": str(e)}

