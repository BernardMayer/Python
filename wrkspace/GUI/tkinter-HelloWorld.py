#!/python
# -*- coding: utf-8 -*-

from tkinter import *

fenetre = Tk()

# Label
label = Label(fenetre, text="Hello, World !")

# Bouton pour action (sortir)
bouton = Button(fenetre, text="Fermer", command=fenetre.quit)

# Bouton radio
val = StringVar()
rbtn1 = Radiobutton(fenetre, text="oui", variable=val, value=1)
rbtn2 = Radiobutton(fenetre, text="non", variable=val, value=2)
rbtn3 = Radiobutton(fenetre, text="chaispas", variable=val, value="?")

# Liste
liste = Listbox(fenetre)
liste.insert(1, "Python")
liste.insert(2, "PHP")
liste.insert(3, "jQuery")
liste.insert(4, "CSS")
liste.insert(5, "EcmaScript")

# Curseur/Scale
val2 = DoubleVar()
curs = Scale(fenetre, variable=val2)

curs.pack()
liste.pack()
rbtn1.pack()
rbtn2.pack()
rbtn3.pack()
bouton.pack()
label.pack()

fenetre.mainloop()