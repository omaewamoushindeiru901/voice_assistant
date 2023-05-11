import speech_recognition as sr
import pandas as pd
import pymorphy2


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говоріть зараз...")
        audio = r.listen(source)
    try:
        # Використовуйте готову ASR-модель
        text = r.recognize_google(audio, language='uk-UA')
        print("Розпізнано текст " + text)
        return text
    except sr.UnknownValueError:
        print("ASR не зміг розпізнати текст")
    except sr.RequestError as e:
        print(f"Помилка {e}")

def search_keywords_in_db(text):
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


