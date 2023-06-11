import json
import pandas as pd
import os
import xml.etree.ElementTree as ET

# Définir le dossier à convertir, le chemin est le dossier où se trouve le fichier xml.
folder_path = r"E:\chatbot\MedQuAD（数据集）\1_CancerGov_QA"

# Définir le nom du fichier CSV à enregistrer
csv_file_name = r"E:\chatbot\Code\output.csv"

# Définir les champs à extraire
columns = ['id', 'question', 'answer']

# Définir une liste vide pour contenir toutes les paires de questions et de réponses
qa_pairs = []




def traverseXML():
    c = 0
    d = 0
    # Parcourt récursivement tous les fichiers XML d'un dossier
    for file_name in os.listdir(folder_path):
            d += 1
            if file_name.endswith(".xml"):
                # Lecture de fichiers XML
                try:
                    tree = ET.parse(os.path.join(folder_path, file_name))
                    root_element = tree.getroot()
                    # Extraction des données
                    for qa_pair in root_element.findall("QAPairs/QAPair"):
                        c += 1
                        question = qa_pair.find("Question")
                        answer = qa_pair.find("Answer")
                        if question is not None and answer is not None:
                            qa = {
                                'id': qa_pair.get('pid'),
                                'question': question.text,
                                'answer': answer.text,
                            }
                            qa_pairs.append(qa)

                    # Sortie des données extraites
                    print(f"Extracted {len(qa_pairs)} QA pairs from {file_name}")

                except Exception as e:
                    # Sauter le fichier actuel en cas d'exception de lecture
                    print(f"Error reading {file_name}: {str(e)}")
                    continue

    # Convertir une liste de paires de questions et de réponses en un objet DataFrame et l'enregistrer dans un fichier CSV.
    df = pd.DataFrame(qa_pairs, columns=columns)
    df.to_csv(csv_file_name, index=False)
    print(c)
    print(d)
import csv

def append_data_to_output():
    input_filenames = ["qa_pairs.csv", "dataset.csv"]
    output_filename = "output.csv"

    # Lire le contenu du fichier d'entrée
    data = []
    for input_filename in input_filenames:
        with open(input_filename, "r", newline="", encoding="utf-8") as input_file:
            reader = csv.reader(input_file)
            data.extend(list(reader))

    # Ajouter les relevés au fichier output.csv
    with open(output_filename, "a", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(data)

    print("Data appended to output.csv successfully.")
#traverseXML()
#append_qapaire_to_output()