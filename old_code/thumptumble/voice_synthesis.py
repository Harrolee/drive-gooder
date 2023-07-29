from TTS.api import TTS

MODEL_NAME = 'tts_models/en/ljspeech/vits--neon'
MODEL_PATH = 'voice_models/LeeMay01'
# MODEL_PATH = '/Users/lee/projects/tumblethump/backend/thumptumble/voice_models/LeeMay01Checkpoint_1013400.pth'
# a multilingual, multi-speaker model: 'tts_models/multilingual/multi-dataset/your_tts'


class TTS_Handler():
    def __init__(self):
        # self.tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)
        self.tts = TTS(model_path=f'{MODEL_PATH}/Checkpoint_1013400.pth',
                       config_path=f'{MODEL_PATH}/config.json', progress_bar=False, gpu=False)

    def run_tts(self, text: str, file_path: str):
        self.tts.tts_to_file(text=text, file_path=file_path)
