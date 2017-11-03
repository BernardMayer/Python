#!/python
# -*- coding: utf-8 -*-

## http://www.jchr.be/python/tkinter.htm
## voir 4.2 PanedWindow

# import tkinter as Tkinter
# racine0=Tkinter.Tk()
# racine0.geometry("400x300")
# division0=Tkinter.PanedWindow(orient=Tkinter.VERTICAL)
# division0.pack(expand="yes", fill="both")
# panneau1=Tkinter.Label(division0, text="Panneau Un")
# division0.add(panneau1)
# panneau2=Tkinter.Label(division0, text="Panneau Deux")
# division0.add(panneau2)
# panneau3=Tkinter.Label(division0, text="Panneau Trois")
# division0.add(panneau3)
# racine0.mainloop()

import tkinter as  Tkinter
racine0=Tkinter.Tk()
racine0.geometry("400x300")
division0=Tkinter.PanedWindow(orient=Tkinter.VERTICAL)
division0.pack(expand="yes", fill="both")
haut0=Tkinter.Label(division0, text="Panneau du haut")
division0.add(haut0)
milieu0=Tkinter.Label(division0, text="Panneau du milieu")
division0.add(milieu0)
bas0=Tkinter.PanedWindow(orient=Tkinter.HORIZONTAL) # nouvelle division
bas0.pack(expand="yes", fill="both")
gauche=Tkinter.Label(bas0, text="Panneau bas-gauche")
bas0.add(gauche)
droit=Tkinter.Label(bas0, text="Panneau bas-droit")
bas0.add(droit)
division0.add(bas0) # on acheve la declaration du panneau bas
racine0.mainloop()
