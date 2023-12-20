import hashlib
import os

from elevenlabs import Voice
from elevenlabs import VoiceSettings
from elevenlabs import generate
from elevenlabs import play
from elevenlabs import set_api_key
from elevenlabs import voices

from trainr.backend.handler.motivation.quotes.mr_t import goodbyes
from trainr.backend.handler.motivation.quotes.mr_t import greetings
from trainr.backend.handler.motivation.quotes.mr_t import quotes

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))
import noisereduce as nr
from scipy.io import wavfile


def save_audio(text, text_type, coach, voice: Voice):
    voice_id = voice.voice_id
    file_name = f"elevenlabs-{text_type}-{voice_id}-{hashlib.md5(text.encode()).hexdigest()}.wav"
    dir_path = os.path.join("resources", "narration", coach, text_type)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path,file_name)

    if not os.path.exists(file_path):
        audio = generate(text, voice=voice)

        with open(file_path, "wb") as f:
            f.write(audio)

    return file_path


def denoise_file(file_path):
    # load data
    print(file_path)
    rate, data = wavfile.read(file_path)
    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(f"denoised-{file_path}", rate, reduced_noise)


mr_t_voice_id = 'kCDGrDEQuS9NTaD5fxkl'

mr_t_voice = Voice(
    voice_id=mr_t_voice_id,
    name="Mr T",
    settings=VoiceSettings(
        stability=0.4, similarity_boost=0.2, style=0.2, use_speaker_boost=True
    ),
)

for quote in quotes:
    file = save_audio(quote, 'motivation', 'mr_t', mr_t_voice)
    denoise_file(file)
    break

for quote in greetings:
    file = save_audio(quote, 'hello', 'mr_t', mr_t_voice)
    denoise_file(file)
    break

for quote in goodbyes:
    file = save_audio(quote, 'goodbye', 'mr_t', mr_t_voice)
    denoise_file(file)
    break
