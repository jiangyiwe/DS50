from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

import chatNLTK

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

        def send_message():
            message = input_box.get("1.0",'end-1c')
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

        send_button = Button(input_frame, text="Envoyer", command=send_message)
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


