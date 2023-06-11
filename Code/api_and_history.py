import re
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import sys


def search_on_nlm_api(search_term):
    db = "healthTopics"

    # Créer des URL de demande d'API
    url = f"https://wsearch.nlm.nih.gov/ws/query?db={db}&term={search_term}"

    # Envoi de requêtes API
    response = requests.get(url)
    # Traitement des réponses de l'API
    if response.status_code == 200:
        # Analyse des réponses XML
        root = ET.fromstring(response.content)

        # Extraction des données nécessaires
        documents = root.findall('list/document')


        if len(documents) > 0:
            # Sélectionner le premier document à traiter
            document = documents[0]
            url = document.get('url')
            title_element = document.find('content[@name="title"]')
            title = title_element.text if title_element is not None else "N/A"
            summary_element = document.find('content[@name="FullSummary"]')
            summary = summary_element.text if summary_element is not None else "N/A"

            if url == "https://medlineplus.gov/evaluatinghealthinformation.html":
                return None, None, None

            # Manipulation des balises HTML
            if title is not None:
                title = BeautifulSoup(title, "html.parser").get_text()
            if summary is not None:
                summary = BeautifulSoup(summary, "html.parser").get_text()

            # Analyse des URL
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

            # Traitement ultérieur ou présentation des données ici
            print("URL:", url)
            print("Title:", title)


        else:
            url = "N/A"
            title = "N/A"
            summary = "N/A"


        return title, summary, url

    else:
        print("API request fail")
        return None, None, None

# Définir le chemin d'accès au fichier CSV à créer
history_file = 'E:\chatbot\Code\history.csv'


# Définir des fonctions pour mettre à jour l'historique
def update_history(user_input, result):
    # Vérifier si le fichier existe déjà
    if not os.path.isfile(history_file):
        # Créer un fichier CSV vide et écrire les titres des colonnes
        with open(history_file, 'w') as file:
            file.write("Question,Answer\n")

    # Charger le fichier historique (s'il existe)
    if os.path.isfile(history_file):
        history_df = pd.read_csv(history_file)
    else:
        history_df = pd.DataFrame(columns=['Question', 'Answer'])

    # Ajouter un nouvel enregistrement au DataFrame Historique
    new_record = pd.DataFrame({'Question': [user_input], 'Answer': [result]})

    # Ajouter de nouveaux enregistrements au fichier CSV
    new_record.to_csv(history_file, index=False, header=False, mode='a')


# Définir la fonction de visualisation de l'historique
def view_history(history_file):
    # Chargement du dernier historique à partir du fichier d'historique
    history_df = pd.read_csv(history_file)

    # Obtenir les 10 derniers enregistrements
    recent_history = history_df.tail(10)

    # Conversion des enregistrements historiques au format dictionnaire
    history_dict = recent_history.to_dict(orient='records')

    return history_dict

# La fonction view_history() est appelée dans la fonction de routage pour récupérer l'historique.

# La fonction search_on_website() est appelée dans la logique du chatbot pour rechercher et obtenir des résultats.

"""
while True:
    print("Bot:Hello, what can I do for you?")
    user_input = input("You: ")

    # 检查用户输入是否为 "exit"
    if user_input == "exit":
        print("Bot: Goodbye!")

    elif user_input == "history":
    # 调用 view_history() 函数来获取历史记录
        history = view_history(history_file)
        for record in history:
            print(f"Question: {record['Question']}")
            print(f"Answer: {record['Answer']}")
            print("----------")
        sys.exit()  # 退出进程


    print("Do you want to search it on website?y/n")

    user_input_choose=input("You: ")

    if user_input_choose.lower == "yes" or "y":

      title, summary, url = search_on_nlm_api(user_input)

      if summary is not None:
        result = re.sub(r'<[^>]+>', '', summary)
        print("Bot: " + result)
        # 保存历史记录
        update_history(user_input, result)
      else:
        print("Bot: Sorry, I couldn't find any relevant information.")

    ##if user_input_choose.lower == "n" or "no":
"""






