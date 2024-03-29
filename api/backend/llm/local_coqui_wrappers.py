from TTS.api import TTS
import random
import string
import os

model: str = "tts_models/en/vctk/vits"
speaker: str = "p225"

tts = TTS(model)

def text_to_speech(text: str, emotion: str, speed: float):
    path = _build_temporary_file_path()
    tts.tts_to_file(text=text, speaker=speaker, file_path=path, emotion=emotion, speed=speed)

    file_handle = open(path, 'rb')
    try:
        return file_handle.read()
    finally:
        file_handle.close()
        os.remove(path)

def _build_temporary_file_path():
    output_path = os.path.join(_get_current_path(), "..", "..", "output")

    if(not os.path.isdir(output_path)):
        try:
            os.mkdir(output_path)
        except Exception as err:
            print(f"Could not create output dir at {output_path}.\nError message:\n{err}",file=SystemError)
    assert os.path.isdir(output_path), f"Gah! Somehow the path below does not exist\n{output_path}"

    filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    return os.path.join(output_path, f'{filename}.wav')

def _get_current_path():
    return os.path.dirname(os.path.realpath(__file__))