#!/python
# -*- coding: utf-8 -*-
"""
Lance une interface GUI de connexion 
a un outil decisionnel [pour un adherent]
"""

from myApp_mod import *
from config import *
# from tkinter import *
# from tkinter.messagebox import *



def main() :
    topDepart = pointeuse()
    pid = str(os.getpid())
    log("--- \nINFO : Top depart : [" + topDepart + "] avec le PID [" + pid + "]")
    print("--- \nTop depart : [" + topDepart + "] avec le PID [" + pid + "]")

    ## 
    ##  Lire la config
    ##
    ini = lireConfig()
    
    gui_02(ini, actions)
    







    #log("INFO : - - - - - - - Fin de traitement - - - - - - - ")
    if (ini['verbose']) : 
        print("INFO : - - - - - - - Fin de traitement - - - - - - - ")
        
    topFin = pointeuse()
    log("INFO : Top fin : [" + topFin + "]")
    print("Top fin : [" + topFin + "]")

    exit(0)

if __name__ == '__main__':
    main()