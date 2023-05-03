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

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


#数据预处理
def preprocess_data(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))#去除常用字
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()#词性还原
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return ' '.join(lemmatized_tokens)

def find_best_match(input_text, corpus_tfidf, tfidf_vectorizer):
    input_tfidf = tfidf_vectorizer.transform([input_text])
    similarity_scores = cosine_similarity(input_tfidf, corpus_tfidf)
    best_match_index = np.argmax(similarity_scores)
    best_match_question = df.loc[best_match_index, 'question']
    best_match_answer = df.loc[best_match_index, 'answer']
    return best_match_question, best_match_answer

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
