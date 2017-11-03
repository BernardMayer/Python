#!/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *


def alert() :
    showinfo("Alerte", "???")

f = Tk()
f.geometry("800x600+80+60")

# Menu
menubar = Menu(f)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouveau", command=alert)
menu1.add_command(label="Ouvrir", command=alert)
menu1.add_command(label="chaispas", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=f.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Copier", command=alert)
menu2.add_command(label="Couper", command=alert)
menu2.add_command(label="Coller", command=alert)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu3)

f.config(menu=menubar)

# label = Label(f, text="Hello, World !")
# label.pack()

## Disposition en 2 panneaux l'un sur l'autre,
## Celle du dessous divisee en 2, 
## grande partie gauche avec grille de choix Adherent
## petite partie droite avec choix de l'action


pwParent = PanedWindow(f, orient=VERTICAL)
pwParent.pack(expand=Y, fill=BOTH, pady=2, padx=2) #side=TOP, 
# pwParent.add(Label(pwParent, text="volet 1", background='blue', anchor=CENTER))
# pwParent.add(Label(pwParent, text="volet 2", background='white', anchor=CENTER))
# pwParent.add(Label(pwParent, text="volet 3", background='red', anchor=CENTER))

pwHaut = PanedWindow(pwParent, orient=HORIZONTAL)
pwHaut.add(LabelFrame(pwHaut, text="Outil decisionnel - Aide a la connexion", height=100))
#pwHaut.add(Label(text = "Outil decisionnel - Aide a la connexion"))
pw = PanedWindow(pwParent, orient=HORIZONTAL)
pw.add(LabelFrame(pw, text="Choisir un Adherent, puis l'action a faire"), height=400)
#pw.add(Label(text = "Choisir un Adherent, puis l'action a faire"))
pwBas = PanedWindow(pwParent, orient=HORIZONTAL)
pwBas.add(LabelFrame(pwBas, text="Choisir un Adherent, puis l'action a faire"))
#pwBas.add(Label(text = "message eventuel"))



pwParent.add(pwHaut)
pwParent.add(pw)
pwParent.add(pwBas)

pwParent.pack()
#pw = PanedWindows(pwParent, orient=VERTICAL)

f.mainloop()