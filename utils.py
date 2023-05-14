import nemo.collections.asr as nemo_asr
import pandas as pd
import speech_recognition as sr
from uk_stemmer import UkStemmer

batch_size = 16

model = nemo_asr.models.EncDecCTCModel.restore_from("model.nemo")
model.eval()


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говоріть зараз...")
        audio = r.listen(source)

    with open("audio.wav", "wb") as f:
        f.write(audio.get_wav_data(convert_rate=16000, convert_width=2))
    predictions = model.transcribe(["audio.wav"], batch_size=batch_size)
    prediction = ""
    for pr in predictions:
        prediction += str(pr)

    return prediction.replace("▁", " ")


def search_keywords_in_db(text):
    text = remove_words_from_string(text, 'misc_words.csv')
    df = pd.read_csv('clothes_database.csv')
    stemmer = UkStemmer()
    lemmas = [stemmer.stemWord(keyword) for keyword in text.split()]
    print("lemmas: ", lemmas)

    names_list = set([name.lower() for name in df['Назва'].tolist()])

    search_results = set()
    found = False

    for index, row in df.iterrows():
        found_keywords = []
        for lemma in lemmas:
            if (lemma.lower() in row['Назва'].lower()) or (lemma.lower() in row['Бренд'].lower()) or (
                    lemma.lower() in row['Колір'].lower()) or (lemma.lower() in row['Розмір'].lower()):
                found_keywords.append(lemma)
        if len(found_keywords) == len(lemmas):
            search_results.add(row['Полиця'])
            found = True

    if not found:
        for lemma in lemmas:
            for name in names_list:
                if lemma in name:
                    print(lemma)
                    search_results = set(df['Полиця'][df['Назва'].str.lower().str.contains(lemma.lower())])
                    break
            if search_results:
                break
    search_results = sorted(list(search_results))
    return search_results, found


def remove_words_from_string(string, words_file):
    with open(words_file, encoding='utf-8') as f:
        words = f.readline().split(',')
    for word in words:
        string = string.replace(str(word), '')
    return string
