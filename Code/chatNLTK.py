import os
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from collections import defaultdict
import pprint
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import speech_recognition as sr

#Prétraitement des données
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please start talking...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='en-US')
        print("Identification of results：", text)
        return text
    except sr.UnknownValueError:
        print("Audio not recognised")
    except sr.RequestError as e:
        print("An error occurred with the request：", str(e))

    return None

def ask_question():
    while True:
        choice = input("Please select the method of questioning (voice/text)：")
        if choice.lower() == 'Audio':
            question = recognize_speech()
            if question:
                return question
        elif choice.lower() == 'Text':
            question = input("Please enter a question：")
            return question
        else:
            print("Invalid selection, please re-enter")

def preprocess_data(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))#Suppression des mots communs
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()#Réduction lexicale
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return ' '.join(lemmatized_tokens)

def find_best_match(input_text, corpus_tfidf, tfidf_vectorizer):
    input_tfidf = tfidf_vectorizer.transform([input_text])
    similarity_scores = cosine_similarity(input_tfidf, corpus_tfidf)
    best_match_index = np.argmax(similarity_scores)
    best_match_score = similarity_scores[0, best_match_index]

    if best_match_score < 0.5:  # Définir un seuil pour déterminer s'il y a suffisamment de correspondances de similarité
        # Aucun résultat n'a été trouvé pour la question Essayez de trouver des synonymes pour la question
        synonyms = text_parser_synonym_antonym_finder(input_text)
        for synonym in synonyms:
            synonym_tfidf = tfidf_vectorizer.transform([synonym])
            synonym_scores = cosine_similarity(synonym_tfidf, corpus_tfidf)
            synonym_match_index = np.argmax(synonym_scores)
            synonym_match_score = synonym_scores[0, synonym_match_index]

            if synonym_match_score >= 0.5:  # Définir un seuil pour déterminer s'il y a suffisamment de correspondances de similarité
                best_match_index = synonym_match_index
                best_match_score = synonym_match_score
                break

    if best_match_score < 0.5:
        return None  # Aucune question ou réponse correspondante n'a été trouvée

    best_match_question = df.loc[best_match_index, 'question']
    best_match_answer = df.loc[best_match_index, 'answer']
    return best_match_question, best_match_answer



def text_parser_synonym_antonym_finder(text: str):
    tokens = word_tokenize(text)
    synonyms = defaultdict(list)
    antonyms = defaultdict(list)
    for token in tokens:
        for syn in wordnet.synsets(token):
            for i in syn.lemmas():
                # synonyms.append(i.name())
                # print(f'{token} synonyms are: {i.name()}')
                synonyms[token].append(i.name())
                if i.antonyms():
                    # antonyms.append(i.antonyms()[0].name())
                    # print(f'{token} antonyms are: {i.antonyms()[0].name()}')
                    antonyms[token].append(i.antonyms()[0].name())
    return synonyms



def load_corpus():
    df = pd.read_csv('E:\chatbot\Code\output.csv', encoding='utf-8',
                     names=['id', 'question', 'answer'])
    corpus = df['question'].tolist()
    preprocessed_corpus = [preprocess_data(text) for text in corpus]
    tfidf_vectorizer = TfidfVectorizer()
    corpus_tfidf = tfidf_vectorizer.fit_transform(preprocessed_corpus)
    return df, corpus_tfidf, tfidf_vectorizer



df, corpus_tfidf, tfidf_vectorizer = load_corpus()
"""
while True:
    question = ask_question()
    if question:
        preprocessed_question = preprocess_data(question)
        best_match = find_best_match(preprocessed_question, corpus_tfidf, tfidf_vectorizer)
        if best_match:
            best_match_question, best_match_answer = best_match
            print("匹配问题：", best_match_question)
            print("回答：", best_match_answer)
        else:
            print("没有找到匹配的问题和答案。")

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = input('You: ')
    preprocessed_input = preprocess_data(user_input)
    best_match_question, best_match_answer = find_best_match(preprocessed_input, corpus_tfidf, tfidf_vectorizer)
    response = best_match_answer
    print('Chatbot:', response)

while True:
    user_input = input("You: ")
    preprocessed_input = preprocess_data(user_input)
    best_match_question, best_match_answer = find_best_match(preprocessed_input, corpus_tfidf, tfidf_vectorizer)
    print("Bot: " + best_match_answer)
"""