from backend.request_models import ReadTextRequestDto
from TTS.api import TTS

model: str = "tts_models/en/vctk/vits"
speaker: str = "p225"
tts = TTS(model)


def get_audio_for_text_handler(text: ReadTextRequestDto):
    generate_tts(text=text.text, filepath="",
                 emotion=text.emotion, speed=text.speed)
    return text.text


def generate_tts(text: str, filepath: str, emotion: str, speed: float):
    tts.tts_to_file(text=text, speaker=speaker,
                    file_path=filepath, emotion=emotion, speed=speed)
