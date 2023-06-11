import re
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import speech_recognition as sr
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import chatNLTK
from tkinter import Button
import api_and_history
class main_window:
    def __init__(self, master):
        self.master = master
        master.update_idletasks()
        master.title("Chatbot")
        # set window width and height
        master.configure(width=900, height=600)
        ico = Image.open(r"E:\chatbot\Code\ressources\chatbot.png")
        photo = ImageTk.PhotoImage(ico)
        master.wm_iconphoto(False, photo)
        # set window background color
        master.configure(bg='#2F6C60')
        master.attributes('-alpha', 1)
        # move window center
        winWidth = master.winfo_reqwidth()
        winHeight =  master.winfo_reqheight()
        posRight = int( master.winfo_screenwidth() / 2 - winWidth / 2)
        posDown = int( master.winfo_screenheight() / 2 - winHeight / 2)
        master.geometry("+{}+{}".format(posRight, posDown))
        chatbot_label = Label( master, text="Chatbot", bg='#2F6C60',
                              font=("Trebuchet Ms", 30, "bold"), fg="white")
        chatbot_label.place(x=380, y=25)

        bttn(370, 150, "ressources/startbutton.png", "ressources/startbutton_2.png", self.open_start_window,self.master)
        bttn(370, 300, "ressources/settingsbtn.png", "ressources/settingbutton_2.png", cmd1,self.master)
        bttn(370, 450, "ressources/introbtn.png", "ressources/introbutton_2.png", self.open_intro_window,self.master)

    def open_intro_window(self):
        self.new_window = Toplevel(self.master)
        self.app = IntroWindow(self.new_window)

    def open_start_window(self):
        self.new_window = Toplevel(self.master)
        self.app = StartWindow(self.new_window)

class IntroWindow:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        # set window width and height
        master.configure(width=900, height=600)
        ico = Image.open(r"E:\chatbot\Code\ressources\chatbot.png")
        photo = ImageTk.PhotoImage(ico)
        master.wm_iconphoto(False, photo)
        # set window background color
        master.configure(bg='#2F6C60')
        master.attributes('-alpha', 1)
        # move window center
        winWidth = master.winfo_reqwidth()
        winHeight = master.winfo_reqheight()
        posRight = int(master.winfo_screenwidth() / 2 - winWidth / 2)
        posDown = int(master.winfo_screenheight() / 2 - winHeight / 2)
        master.geometry("+{}+{}".format(posRight, posDown))
        chatbot_label = Label(master, text="Introduction", bg='#2F6C60',
                              font=("Trebuchet Ms", 30, "bold"), fg="white")
        chatbot_label.place(x=330, y=25)

        label1 = Label(master, text="Il s'agit d'un chatbot que vous pouvez utiliser pour poser des questions sur la santé et qui ",bg='#2F6C60', font=("Trebuchet Ms", 16), fg="white")
        label1.place(x=40, y=120)
        label2 = Label(master, text="vous donnera une réponse de base.",bg='#2F6C60', font=("Helvetica", 16), fg="white")
        label2.place(x=30, y=160)

        label3 = Label(master, text="Veuillez noter que le chatbot ne remplace pas un médecin professionnel et que vous devez ", bg='#2F6C60',font=("Trebuchet Ms", 16), fg="white")
        label3.place(x=40, y=230)

        label4 = Label(master,
                       text="en consulter un en cas de problème.",
                       bg='#2F6C60', font=("Helvetica", 16), fg="white")
        label4.place(x=30, y=270)
        bttn(700, 450, "ressources/quitbtn.png", "ressources/quitbutton_2.png", self.close_window,self.master)

    def close_window(self):
        self.master.destroy()

class StartWindow:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        # set window width and height
        master.configure(width=900, height=600)
        ico = Image.open(r"E:\chatbot\Code\ressources\chatbot.png")
        photo = ImageTk.PhotoImage(ico)
        master.wm_iconphoto(False, photo)
        # set window background color
        master.configure(bg='#2F6C60')
        master.attributes('-alpha', 1)
        # move window center
        winWidth = master.winfo_reqwidth()
        winHeight = master.winfo_reqheight()
        posRight = int(master.winfo_screenwidth() / 2 - winWidth / 2)
        posDown = int(master.winfo_screenheight() / 2 - winHeight / 2)
        master.geometry("+{}+{}".format(posRight, posDown))
        chat_box = Text(self.master, width=90, height=30)
        chat_box.config(state=DISABLED)
        chat_box.grid(row=0, column=0, padx=120, pady=45)
        input_frame = Frame(self.master)
        input_frame.grid(row=1, column=0, padx=5, pady=10)

        input_box = Text(input_frame, width=70,height=3)
        input_box.pack(side=LEFT)

        def recognize_speech():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                chat_box.config(state=NORMAL)
                chat_box.insert(END, "Vous: " + "Please start talking..." + "\n", ('usertxt', 'bold1'))
                chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                chat_box.tag_configure('usertxt', foreground='#006400')
                chat_box.config(state=DISABLED)
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language='en-US')
                chat_box.config(state=NORMAL)
                chat_box.insert(END, "Identification of results：" +text+ "\n", ('usertxt', 'bold1'))
                chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                chat_box.tag_configure('usertxt', foreground='#006400')
                chat_box.config(state=DISABLED)
                return text
            except sr.UnknownValueError:
                chat_box.config(state=NORMAL)
                chat_box.insert(END, "Audio not recognised" + "\n", ('usertxt', 'bold1'))
                chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                chat_box.tag_configure('usertxt', foreground='#006400')
                chat_box.config(state=DISABLED)
            except sr.RequestError as e:
                chat_box.config(state=NORMAL)
                chat_box.insert(END, "An error occurred with the request：" + "\n", ('usertxt', 'bold1'))
                chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                chat_box.tag_configure('usertxt', foreground='#006400')
                chat_box.config(state=DISABLED)

        def send_message():
            message = input_box.get("1.0", 'end-1c')

            if message.strip() != "":
                chat_box.config(state=NORMAL)
                chat_box.insert(END, "Vous: " + message + "\n", ('usertxt','bold1'))
                chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                chat_box.tag_configure('usertxt', foreground='#006400')
                chat_box.config(state=DISABLED)
                input_box.delete('1.0', END)
                preprocessed_input = chatNLTK.preprocess_data(message)
                best_match_question, best_match_answer = chatNLTK.find_best_match(preprocessed_input,
                                                                                  chatNLTK.corpus_tfidf,
                                                                                  chatNLTK.tfidf_vectorizer)
                response = best_match_answer
                #print('Chatbot:', response)
                chat_box.config(state=NORMAL)
                chat_box.insert(END, "Chatbot: " + response + "\n", ('chatbottxt','bold2'))
                chat_box.tag_configure('bold2', font=('Arial', 12, 'bold'))
                chat_box.tag_configure('chatbottxt', foreground='#00008B')
                chat_box.config(state=DISABLED)
            else:
                messagebox.showwarning("Warning", "Veuillez entrer un message!")

        def voice_question():
            question = recognize_speech()
            chat_box.config(state=NORMAL)
            chat_box.insert(END, "Vous: " + question + "\n", ('usertxt', 'bold1'))
            chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
            chat_box.tag_configure('usertxt', foreground='#006400')
            chat_box.config(state=DISABLED)
            input_box.delete('1.0', END)
            preprocessed_question = chatNLTK.preprocess_data(question)
            best_match_question, best_match_answer = chatNLTK.find_best_match(preprocessed_question, chatNLTK.corpus_tfidf, chatNLTK.tfidf_vectorizer)
            response = best_match_answer
            # print('Chatbot:', response)
            chat_box.config(state=NORMAL)
            chat_box.insert(END, "Chatbot: " + response + "\n", ('chatbottxt', 'bold2'))
            chat_box.tag_configure('bold2', font=('Arial', 12, 'bold'))
            chat_box.tag_configure('chatbottxt', foreground='#00008B')
            chat_box.config(state=DISABLED)

        def search_on_nlm_api(search_term):
            db = "healthTopics"

            # Construire des URL de demande d'API
            url = f"https://wsearch.nlm.nih.gov/ws/query?db={db}&term={search_term}"

            # Envoi de requêtes API
            response = requests.get(url)
            # Gestion des réponses de l'API
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
                    chat_box.config(state=NORMAL)
                    chat_box.insert(END, "URL:"+url + "\n",
                                    ('usertxt', 'bold1'))
                    chat_box.tag_configure('bold2', font=('Arial', 12, 'bold'))
                    chat_box.tag_configure('chatbottxt', foreground='#00008B')
                    chat_box.insert(END, "Title:"+ title + "\n",
                                    ('usertxt', 'bold1'))
                    chat_box.tag_configure('bold2', font=('Arial', 12, 'bold'))
                    chat_box.tag_configure('chatbottxt', foreground='#00008B')
                    chat_box.config(state=DISABLED)



                else:
                    url = "N/A"
                    title = "N/A"
                    summary = "N/A"

                return title, summary, url

            else:
                print("API request fail")
                return None, None, None

        def read_website():
            user_input = input_box.get("1.0", 'end-1c')
            input_box.delete('1.0', END)
            if user_input == "history":
                view_history_window()
                return
            else:
                title, summary, url = search_on_nlm_api(user_input)
                if summary is not None:
                    result = re.sub(r'<[^>]+>', '', summary)
                    chat_box.config(state=NORMAL)
                    chat_box.insert(END, "Vous: "+ user_input+ "\n",
                                    ('usertxt', 'bold1'))
                    chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                    chat_box.tag_configure('usertxt', foreground='#006400')
                    chat_box.insert(END, "Chatbot: " + result + "\n",
                                    ('usertxt', 'bold1'))
                    chat_box.tag_configure('bold2', font=('Arial', 12, 'bold'))
                    chat_box.tag_configure('chatbottxt', foreground='#00008B')
                    chat_box.config(state=DISABLED)
                    # 保存历史记录
                    api_and_history.update_history(user_input, result)
                else:
                    chat_box.config(state=NORMAL)
                    chat_box.insert(END, "Chatbot: "+"Sorry, I couldn't find any relevant information." + "\n",
                                    ('usertxt', 'bold1'))
                    chat_box.tag_configure('bold1', font=('Times', 16, 'bold italic'))
                    chat_box.tag_configure('usertxt', foreground='#006400')
                    chat_box.config(state=DISABLED)
        def view_history_window():
            # Appeler la fonction view_history() pour obtenir l'historique
            history = api_and_history.view_history(api_and_history.history_file)
            history_text = ""
            for record in history:
                history_text += f"Question: {record['Question']}\n"
                history_text += f"Answer: {record['Answer']}\n"
                history_text += "----------\n"
            # Créer une nouvelle fenêtre pour afficher l'historique
            history_window = Toplevel(self.master)
            history_label = Label(history_window, text=history_text)
            history_label.pack()

        voice_button = Button(input_frame, text="Ask a question by voice", command=voice_question)
        voice_button.pack(side=LEFT, padx=5)
        read_button = Button(input_frame, text="Read from website", command=read_website)
        read_button.pack(side=LEFT, padx=5)
        send_button = Button(input_frame, text="Send", command=send_message)
        send_button.pack(side=LEFT, padx=5)
        exit_button = Button(input_frame, text="Exit", command=self.close_window)
        exit_button.pack(side=LEFT, padx=10)



    def close_window(self):
        self.master.destroy()

def bttn(x, y, img1, img2, cmd,root):
    # image = ImageTk.PhotoImage(Image.open(img1))
    image1 = Image.open(img1)
    image2 = Image.open(img2)
    # Resize the image in the given (width, height)
    img1 = image1.resize((160, 60))
    img2 = image2.resize((160, 60))
    # Conver the image in TkImage
    my_img1 = ImageTk.PhotoImage(img1)
    my_img2 = ImageTk.PhotoImage(img2)

    # image_a=ImageTk.PhotoImage(Image.open(img1))
    # image_b = ImageTk.PhotoImage(Image.open(img2))
    def on_enter(e):
        mybtn['image'] = my_img2

    def on_leave(e):
        mybtn['image'] = my_img1

    mybtn = Button(root, image=my_img1, border=0, cursor='arrow', command=cmd, relief=SUNKEN, borderwidth=0,
                   bg='#2F6C60')
    mybtn.bind("<Enter>", on_enter)
    mybtn.bind("<Leave>", on_leave)
    mybtn.place(x=x, y=y)


def cmd1():
    print('hello world')

root = Tk()
app = main_window(root)
#app = StartWindow(root)
root.mainloop()


