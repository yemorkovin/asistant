import torch
import sounddevice as sd


class Silero_:
    def __init__(self):
        self.device = torch.device('cpu')
        self.model, self.text = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language='ru',
            speaker='v3_1_ru'
        )
        self.model.to(self.device)
        self.sample_rate = 48000


    def silero_tts_basic(self, text, speaker='aidar'):
        audio = self.model.apply_tts(
            text=text,
            speaker=speaker,
            sample_rate=self.sample_rate,
            put_accent=True,
            put_yo=True
        )

        sd.play(audio, self.sample_rate)
        sd.wait()
