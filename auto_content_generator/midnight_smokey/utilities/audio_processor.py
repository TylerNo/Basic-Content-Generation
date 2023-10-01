import subprocess as sp
import soundfile as sf
from pedalboard import Pedalboard, Reverb
from math import trunc
import numpy as np
import os


def start_audio_processor(room_size=0.75,
                          damping=0.5,
                          wet_level=0.08,
                          dry_level=0.2,
                          delay=2,
                          slowfactor=0.08):
    try:
        audio = "auto_content_generator/midnight_smokey/assets/temp/audio.mp3"
        output = "auto_content_generator/midnight_smokey/assets/temp/output.wav"
        if '.wav' not in audio:
            with open(os.devnull, 'wb') as devnull:
                sp.call(f'ffmpeg -i "{audio}" tmp.wav', shell=True, stdout=devnull, stderr=sp.STDOUT)
            audio = 'tmp.wav'

        audio, sample_rate = sf.read(audio)
        sample_rate -= trunc(sample_rate * slowfactor)

        # Add reverb
        board = Pedalboard([Reverb(
            room_size=room_size,
            damping=damping,
            wet_level=wet_level,
            dry_level=dry_level
        )])

        effected = board(audio, sample_rate)
        channel1 = effected[:, 0]
        channel2 = effected[:, 1]
        shift_len = delay * 1000
        shifted_channel1 = np.concatenate((np.zeros(shift_len), channel1[:-shift_len]))
        combined_signal = np.hstack((shifted_channel1.reshape(-1, 1), channel2.reshape(-1, 1)))

        sf.write(output, combined_signal, sample_rate)
        print("Audio Processing Complete")

        if os.path.exists('tmp.wav'):
            os.remove('tmp.wav')

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
