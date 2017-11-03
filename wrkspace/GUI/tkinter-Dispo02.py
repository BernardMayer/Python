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












f.mainloop()