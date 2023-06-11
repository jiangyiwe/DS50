from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.ttk import Progressbar
import os


i = 0
def loadingwindow():
    loadingwindow = Tk()
    imageWelcome = Image.open(r"E:\chatbot\Code\ressources\welcomeimage.png")
    resized_image= imageWelcome.resize((600,400), Image.LANCZOS)
    new_image= ImageTk.PhotoImage(resized_image)
    loadingwindow.configure(width=900, height=600)
    ico = Image.open(r"E:\chatbot\Code\ressources\chatbot.png")
    photo = ImageTk.PhotoImage(ico)
    loadingwindow.wm_iconphoto(False, photo)
    loadingwindow.title("Chatbot")
    Width = loadingwindow.winfo_reqwidth()
    Height = loadingwindow.winfo_reqheight()
    posRight = int(loadingwindow.winfo_screenwidth() / 2 - Width / 2)
    posDown = int(loadingwindow.winfo_screenheight() / 2 - Height / 2)
    loadingwindow.geometry("+{}+{}".format(posRight, posDown))
    #loadingwindow.overrideredirect(True)
    loadingwindow.configure(bg='#2F6C60')
    welcome_label = Label(loadingwindow,text="Chatbot Vous Souhaite La Bienvenue",bg='#2F6C60',font=("Trebuchet Ms",20,"bold"),fg="#FFFFFF")
    welcome_label.place(x=225,y=25)
    bg_label = Label(loadingwindow, image=new_image,bg='#2F6C60')
    bg_label.place(x=100,y=65)
    progress_label= Label(loadingwindow,text="Loading...",font=("Trebuchet Ms",15,"bold"),fg="#FFFFFF",bg='#2F6C60')
    progress_label.place(x=380,y=430)
    progress = ttk.Style()
    progress.theme_use('vista')
    progress.configure("red.Horizontal.TProgressbar",bg = "#108cff")
    progress = Progressbar(loadingwindow,orient=HORIZONTAL,length=400,mode='determinate',style="red.Horizontal.TProgressbar")
    progress.place(x=230,y=480)

    def top():
        loadingwindow.withdraw()
        os.system("python Rootwindow.py")
        loadingwindow.destroy()
    def load():
        global i
        if i <= 10:
            txt = "Loading..." + (str(10 * i) + '%')
            progress_label.config(text=txt)
            progress_label.after(600, load)
            progress['value'] = 10 * i
            i += 1
        else:
            top()
    load()
    loadingwindow.resizable(False,False)
    loadingwindow.mainloop()

