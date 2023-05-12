import nemo.collections.asr as nemo_asr
import numpy as np
import pandas as pd
import pymorphy2
import speech_recognition as sr
import torch
import torchaudio
from transformers import Wav2Vec2Processor
import pyaudio
import wave
import io
from pydub import AudioSegment
from pydub.utils import make_chunks

batch_size = 16
import logging

logging.getLogger("NeMo").setLevel(logging.WARNING)

'''def recognize_speech():
    # Завантаження моделі
    model = nemo_asr.models.EncDecCTCModel.load_from_checkpoint("model.ckpt")
    model.eval()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говоріть зараз...")
        audio = r.listen(source)
        # Convert audio data to PyTorch tensor
    audio_np = np.frombuffer(audio.frame_data, dtype=np.int16)
    audio_tensor = torch.from_numpy(audio_np).unsqueeze(0).float()
   # audio_tensor = audio_tensor.set_channels(1)
    # Transcribe the audio files
    predictions = model.transcribe(audio_tensor)
    predictions = [prediction.replace('▁', ' ') for prediction in predictions]
    print(predictions)
    return predictions'''

import soundfile as sf


def recognize_speech():
    # Load the ASR model
    model = nemo_asr.models.EncDecCTCModel.load_from_checkpoint("model.ckpt")
    model.eval()

    # Record audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говоріть зараз...")
        audio = r.listen(source)

    with open("audio.wav", "wb") as f:
        f.write(audio.get_wav_data(convert_rate=16000, convert_width=2))
    predictions = model.transcribe(["audio.wav"])
    prediction = ""
    for pr in predictions:
        prediction += str(pr)

    return prediction[1:].replace("▁", " ")


def search_keywords_in_db(text):
    text = remove_words_from_string(text, 'misc_words.csv')
    df = pd.read_csv('clothes_database.csv')
    morph = pymorphy2.MorphAnalyzer()
    lemmas = [morph.parse(keyword)[0].normal_form for keyword in text.split()]
    print("lemmas: ", lemmas)
    search_results = set()
    for index, row in df.iterrows():
        found_keywords = []
        for lemma in lemmas:
            if (lemma.lower() in row['Назва'].lower()) or (lemma.lower() in row['Бренд'].lower()) or (
                    lemma.lower() in row['Колір'].lower()) or (lemma.lower() in row['Розмір'].lower()):
                found_keywords.append(lemma)
        if len(found_keywords) == len(lemmas):
            search_results.add(row['Полиця'])
    search_results = sorted(list(search_results))
    return search_results


def remove_words_from_string(string, words_file):
    with open(words_file, encoding='utf-8') as f:
        words = f.readline().split(',')
    for word in words:
        string = string.replace(str(word), '')
    return string
