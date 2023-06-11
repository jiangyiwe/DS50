import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.chat.util import Chat, reflections
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv


def store_dataset_as_csv():
    # Code du crawler web pour extraire les questions et les réponses des sites web
    url = 'https://www.bhf.org.uk/informationsupport/how-a-healthy-heart-works'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    questions = soup.find_all('h2')
    answers = soup.select('h2 + p')

    # Enregistrer les questions et les réponses dans une liste
    dataset = []
    for i in range(len(questions)):
        question_text = questions[i].text.strip()
        answer_text = ""
        next_tag = questions[i].find_next_sibling()
        while next_tag and next_tag.name != 'h2':
            answer_text += next_tag.text.strip() + "\n"
            next_tag = next_tag.find_next_sibling()
        id_text = f"1.{i + 1}"  # Generate id in the format "1.1", "1.2", "1.3", ...
        dataset.append((id_text, question_text, answer_text))  # Add id column
        print(f"ID: {id_text}")
        print(f"Question: {question_text}")
        print(f"Answer: {answer_text.strip()}")
        print()

    # Stockage des listes d'ensembles de données sous forme de fichiers CSV
    csv_filename = 'dataset.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id','Question', 'Answer'])
        writer.writerows(dataset)

    print(f"Dataset stored in {csv_filename}")