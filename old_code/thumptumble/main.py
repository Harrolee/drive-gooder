from fastapi.staticfiles import StaticFiles
import tempfile
import openai  # add your key to the env var OPENAI_API_KEY
import whisper
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from thumptumble.voice_synthesis import TTS_Handler
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import uvicorn
from thumptumble.falcon_inference_entity import Falcon_Handler
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

origins = [
    "http://localhost:3000"
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
# mount a static FE here
app.mount("/static", StaticFiles(directory="/Users/lee/projects/tumblethump/backend/thumptumble/frontendBuild", html=True),
          name='static')

print('🎉 Loaded app 💪')
tts_handler = TTS_Handler()
print('🎉 Loaded TTS 🐸')
llm_handler = Falcon_Handler()
print('🎉 Loaded LLM 🧠')


@app.get('/talk')
async def serve_dummy():
    return RedirectResponse(url="/static/index.html")


@app.post('/talk_llm')
async def talk_llm(audio_data: UploadFile = File(...)):
    transcription = await process_audio(transcribe, audio_data)
    llm_response = await submit_llm(transcription)
    return {"transcription": transcription, "llmResponse": llm_response}


@app.post('/sound_llm')
async def sound_llm(audio_data: UploadFile = File(...)):
    transcription = await process_audio(transcribe, audio_data)
    llm_response = await submit_llm(transcription)
    save_path = tts(llm_response)
    return FileResponse(path=save_path)

    # test with FileResponse and then try a custom response class
    # json_response = {"transcription": transcription, "llmResponse": llm_response}
    # return CustomFileResponse(path=save_path, json_content=json_response, file_content='bytes here')


def transcribe(save_path):
    # hardcode the model config for now
    # we could use large, small, xlarge, non-english, etc
    config = {
        'model': 'base',
    }
    # transcribe audio
    audio_model = whisper.load_model(config['model'])
    result = audio_model.transcribe(save_path)
    return result['text'].strip()


async def save_audio(audio_data: UploadFile = File(...)):
    # TODO: learn how to use tempfile
    save_path = tempfile.mkstemp(text=False)[1]
    with open(save_path, 'wb') as f:
        f.write(await audio_data.read())
    return save_path


async def process_audio(process, audio_data: UploadFile = File(...)):
    save_path = await save_audio(audio_data)
    result = process(save_path)
    Path.unlink(Path(save_path))
    return result


async def submit_llm(prompt: str):
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return chat_completion.choices[0].message.content
    # uncomment below to use Falcon
    # return await llm_handler.predict(prompt)


def tts(text: str):
    save_path = tempfile.mkstemp(suffix='.wav', text=False)[1]
    tts_handler.run_tts(text, save_path)
    return save_path


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("thumptumble.main:app",
                host="localhost", port=8000, reload=True)
