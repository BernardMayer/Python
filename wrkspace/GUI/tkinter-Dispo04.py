#!/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *

from config import *



def alert() :
    showinfo("Alerte", "???")

f = Tk()
#f.geometry("800x600+80+60")

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

##
##  Construction de l'interface
##

Label(f, text=" ").grid(row=0)
Label(f, text="Outil decisionnel : Aide a la connexion").grid(row=1, columnspan=11, sticky=W+E+N+S, padx=5, pady=5) 
Label(f, text=" ").grid(row=2)
##  Les Adherents
a = 0
for r in range(3, 14) :
    Label(f, text=" ").grid(row=r, column=0)
    for c in range(1, 6) :
        if (adherents[a] != "") : 
            Button(f, text=adherents[a], command=lambda: alert(self)).grid(row=r, column=c, padx=2, pady=2, sticky=W+E+N+S)
        else : 
            Label(f, text=" ").grid(row=r, column=c, padx=2, pady=2)
        a += 1
    Label(f, text="").grid(row=r, column=6)
Label(f, text=" ").grid(row=9)
##  Les actions
a = 0
for r in range(3, len(actions) + 3) :
    Label(f, text=" ").grid(row=r, column=0, padx=2, pady=2)
    if (actions[a] != "") :
        Button(f, text=actions[a], command=lambda: alert()).grid(row=r, column=12, padx=2, pady=2, sticky=W+E+N+S)
    else : 
        Label(f, text=" ").grid(row=r, column=12, padx=2, pady=2)
    a += 1

#tBtn = Button(f, text="Test invoke et .bind").grid(row=0, column=0, padx=2, pady=2, sticky=W+E+N+S)
# .bind avec un label...
#tBtn.bind('<1>', lambda e: btn.configure(text="clic gauche"))
#tBtn.invoke()

f.mainloop()