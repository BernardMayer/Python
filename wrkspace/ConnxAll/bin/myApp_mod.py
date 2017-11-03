#!/python
# -*- coding: utf-8 -*-

"""

"""

import sys
import os
import argparse
import configparser
import re
#from collections import OrderedDict
import collections
import datetime
import decimal
import pyodbc
import winreg

from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk

##  Le fichier qui contient le code des actions !
##  Chaque action a une fonction qui porte son nom
from actions import *


##
##  Declarations / Affectations
##

##  Structure container config
dIni = dict()

hidden_val_Adh = ""
hidden_val_act = ""
decimal.getcontext().prec = 2
FileOutSep = "\t"
FileOutHeader = False
Verbose = True
dIni['verbose'] = Verbose


def gui_01(ini, actions) : 
    f = Tk()
    
    Label(f, text=" ").grid(row=0)
    Label(f, text="Outil decisionnel : Aide a la connexion").grid(row=1, columnspan=11, sticky=W+E+N+S, padx=5, pady=5) 
    Label(f, text=" ").grid(row=2)
    ##  Les Adherents
    a = 0
    for r in range(3, 15) :
        Label(f, text=" ").grid(row=r, column=0)
        for c in range(1, 6) :
            #ini['dAdherents_gui'][str(a + 1)]
            if (ini['dAdherents_gui'][str(a + 1)] != "") : 
                Button(f, text=ini['dAdherents_gui'][str(a + 1)], command=lambda: alert(self)).grid(row=r, column=c, padx=2, pady=2, sticky=W+E+N+S)
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
    return

    
def gui_02(ini, actions) : 
    f = Tk()
    gui_num_x = 7
    _row = 0
    
    ##  Les Adherents
    hidden_val_Adh = Entry(f, text="")
    a_max = len(ini['dAdherents_gui'])
    for a in range(0, a_max) : 
        #c = 0
        #Label(f, text=" ").grid(row=r, column=c, padx=2, pady=2)
        #for c in range(1, gui_num_x + 1) : 
        r = a // gui_num_x
        c = a % gui_num_x
        _row = r
        #print("row=" + str(r) + ", col=" + str(c))
        if (ini['dAdherents_gui'][str(a + 1)]) : 
            Button(f, text=ini['dAdherents_gui'][str(a + 1)]['lbl_btn'], command=lambda btnVal = ini['dAdherents_gui'][str(a + 1)]['adhId']: onBtnClick('Adh', btnVal)).grid(row=r, column=c, padx=2, pady=2, sticky=W+E+N+S)
        else : 
            #Label(f, text=" ").grid(row=r, column=c, padx=2, pady=2)
            pass
            #a += 1
        #Label(f, text=" ").grid(column = c + 1)    
    
    ## Separateur
    _row += 1
    ttk.Separator(f, orient='horizontal').grid( column=0, row=_row, columnspan=gui_num_x, sticky='WE', pady=6)

    ## Les actions
    hidden_val_act = Entry(f, text="")
    a_max = len(ini['dActions_gui'])
    _row += 1
    for a in range(0, a_max) : 
        r = a // gui_num_x
        c = a % gui_num_x
        r += _row
        #print("a=" + str(a) + ", _row=" + str(_row) + ", r=" + str(r) + ", col=" + str(c))
        if (ini['dActions_gui'][str(a + 1)]) : 
            Button(f, text=ini['dActions_gui'][str(a + 1)]['lbl_btn'], command=lambda btnVal = ini['dActions_gui'][str(a + 1)]['actId']: onBtnClick('act', btnVal)).grid(row=r, column=c, padx=2, pady=2, sticky=W+E+N+S)
        else : 
            #Label(f, text=" ").grid(row=r, column=c, padx=2, pady=2)
            pass
            #a += 1
        #Label(f, text=" ").grid(column = c + 1)    
    _row += r
    
    ## Separateur
    _row += 1
    # r = _row
    # hidden_val_Adh.grid(row=r, column=0)
    # hidden_val_act.grid(row=r, column=2)
    
    
    
    f.mainloop()  
    return

    
def runAct(Adh, act) : 
    """ Lancement d'une action autonome    """
    if (not Adh) : 
        Adh = "-"
    #print("act=", act)
    try : 
        if (Verbose) : 
            print("INFO : runAct de act=" + act + " et Adh=" + Adh)
        log("INFO : runAct de act=" + act + " et Adh=" + Adh)
        globals()[act](dIni, Adh)
        
    except : 
        if (Verbose) : 
            print("ERREUR : La fonction [" + act + "] est introuvable")
        log("ERREUR : La fonction [" + act + "] est introuvable")
        alert("ERREUR : La fonction [" + act + "] est introuvable")
    # cmd = "act(dIni, None)"
    # eval(cmd)
    #actions.dirUniv(dIni, None)
    
    
def onBtnClick(a, p) :
    """ Le bouton vient d'etre clique, quoi qu'on fait ?    """
    global hidden_val_Adh, hidden_val_act
    if (p in ('remedy', 'dirUniv', 'dirRapp')) : 
        #alert("action autonome")
        runAct(None, p)
        hidden_val_Adh = hidden_val_act = ""
    else : 
        if (a == "Adh") : 
            hidden_val_Adh = p
        elif (a == "act") : 
            hidden_val_act = p
        #print("Adh=" + hidden_val_Adh + ", act=" + hidden_val_act)
        if (len(hidden_val_Adh) > 0 and len(hidden_val_act) > 0) : 
            runAct(hidden_val_Adh, hidden_val_act)
            hidden_val_Adh = hidden_val_act = ""
        

def build_locdata_2tiers(w, h, u) : 
    """ w = where emplacement du repertoire locdata
        h = host
        u = user
    """
    filename = h.replace('.', '_') + ".intranet"
    
    try :
        with open(w + os.sep + filename, "wt" ) as oF :
            oF.write("connection.common.config_name=" + h + "\n") # os.linesep
            oF.write("connection.common.last_authmode=secEnterprise" + "\n")
            oF.write("connection.common.last_user=" + u + "\n")
            oF.write("connection.common.mode=INPROC_CLIENT_MODE" + "\n")
            oF.write("FIN")
    except :
        if (dIni['verbose']) : 
            print("Defaut creation locdata 2tiers dans rep[" + w + "]")
        log("Defaut creation locdata 2tiers dans rep[" + w + "]")


def build_locdata_3tiers(w, h, u) : 
    """ w = where emplacement du repertoire locdata
        h = host
        u = user
    """
    filename = h.replace('.', '_') + "@6400_j2ee.extranet"
    
    try :
        with open(w + "\\" + filename, "wt" ) as oF :
            oF.write("connection.common.config_name=" + h + ":6400" + "\n")
            oF.write("connection.common.last_authmode=secEnterprise" + "\n")
            oF.write("connection.common.last_user=" + u + "\n")
            oF.write("connection.common.mode=HTTP_MODE" + "\n")
            oF.write("connection.http.locale=fr" + "\n")
            oF.write("connection.http.provider=WSTK_HTTP_Tunneling" + "\n")
            oF.write("connection.http.sso_provider=" + "\n")
            oF.write("connection.http.url=http://" + h + "//AnalyticalReporting/../AnalyticalReporting/jsp/shared/WSTKBridge.jsp" + "\n")
            oF.write("connection.http.urlbase=http://" + h + "//AnalyticalReporting/.." + "\n")
            oF.write("connection.http.web_auth_mode=" + "\n")
    except :
        if (dIni['verbose']) : 
            print("Defaut creation locdata 3tiers dans rep[" + w + "]")
        log("Defaut creation locdata 3tiers dans rep[" + w + "]")        

        
def build_dsn(keyVal, clefs) : 
    # print("keyVal =", keyVal)
    # print("dico de clefs=\n", clefs)
    
    try :
        ruche = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_WRITE)
    except : 
        ruche = winreg.CreateKey(winreg.HKEY_CURRENT_USER, keyVal)
    
    ##  Boucler sur le dictionnaire clefs, pour les creer dasn keyVal
    for k, v in clefs.items() :
        #print("k =", k, ", v =", v)
        winreg.SetValueEx(ruche, k, 0, winreg.REG_SZ, v)
    
    winreg.CloseKey(ruche)
    
        
def lireConfig() :
    """ Lire la ligne de commande, y trouver le nom du fichier de configuration
    S'il n'est pas fourni, ce sera le nom du script, suffixé par .ini ou .cfg
    """
    ##  Lire la ligne de commande pour recuperer le fichier ini
    # set dIni['cmdLine'], dIni['iniFile']
    getCmdline()
    
    ##  Lire de fichier de configuration ...
    # set dIni["objCfg"]
    getInifile()
    
    ## En extraire la liste des Adherents ...
    getListeAdherents()
    
    ## En extraire la liste des actions ...
    getListeActions()
    
    ## En extraire les details des actions ...
    getDetailsActions()
    
    
    return dIni

    
def getDetailsActions() : 
    """ A partir de la liste des clefs des actions, recuperer le detail de chacune des actions    """
    # liste des actions
    pass
    
    
def getListeActions() : 
    """ Extraire la liste de Actions du fichier de configuration,
    la trier suivant la valeur de l'info Actions_orderBy du fichier
    """
    
    if (dIni["objCfg"].has_option('ACTIONS', 'Actions_orderBy') and len(dIni["objCfg"]['ACTIONS']['Actions_orderBy'].strip()) > 0) :
        actions_orderBy = dIni["objCfg"]['ACTIONS']['Actions_orderBy'].strip()
    else :
        log("ERREUR : Pour la liste des actions, pas de colonne d'ordonnancement dans le fichier de configuration")
        if (dIni['verbose']) :
            print("ERREUR : Pour la liste des actions, pas de colonne d'ordonnancement dans le fichier de configuration")
        exit()
        
    if (dIni["objCfg"].has_option('ACTIONS', 'actions_fichierListe') and len(dIni["objCfg"]['ACTIONS']['actions_fichierListe'].strip()) > 0) :
        actions_fichierListe = dIni["objCfg"]['ACTIONS']['actions_fichierListe'].strip()
    else :
        log("ERREUR : Pour la liste des actions, pas de fichier dans le fichier de configuration")
        if (dIni['verbose']) :
            print("ERREUR : Pour la liste des actions, pas de fichier dans le fichier de configuration")
        exit()
        
    # Test de la presence du fichier liste Adherents
    if (not os.path.exists(actions_fichierListe)) :
        log("ERROR : Pour la liste des Adherents, le fichier [" + actions_fichierListe + "] est introuvable")
        exit()

        # Lecture du fichier (Les EOL sont presents !)
    try :
        with open(actions_fichierListe, "rt") as fActions :
            lActions_fichier = fActions.readlines()
    except : 
        log("ERREUR : pb lecture fichier [" + actions_fichierListe + "]")
        if (dIni['verbose']) : 
            print("ERREUR : pb lecture fichier [" + actions_fichierListe + "]")
    ##  Constituer la liste des Adherents dans un format attendu par la GUI
    # Quel est l'indice de la colonne de tri ?
    # TODO le separateur dans le fichier de config !
    ligne = lActions_fichier[0].strip().split("\t")
    # TODO si l'indice n'est pas trouve, alors ValueError    
    actions_orderBy_index = ligne.index(actions_orderBy)
    dActions_gui = dict()
    # Suppression de l'entete (elle est dans la variable ligne)
    del lActions_fichier[0]
    for l in lActions_fichier : 
        l = l.strip("\n")
        # if (len(l[0]) == 0) : 
            # continue
        #print("l=" + l)
        action_infos = l.split("\t")
        if (len(action_infos[0]) > 0) :
            dAct = dict()
            #print("Act=" + action_infos[0])
            dAct['actId'] = action_infos[0]
            dAct['lbl_btn'] = action_infos[1]
            dActions_gui[action_infos[actions_orderBy_index]] = dAct
            ##  Les details de l'action sont dans le fichier de configuration
            if (dIni['objCfg'].has_section(dAct['actId'])) : 
                test = dIni['objCfg'][dAct['actId']]
                #print("test=", test)
        else : 
            dActions_gui[action_infos[actions_orderBy_index]] = None
    
    dIni['dActions_gui'] = dActions_gui

    
def getListeAdherents() : 
    """ Extraire la liste de Adherents du fichier de configuration,
    la trier suivant la valeur de l'info Adherents_orderBy du fichier
    """
    
    if (dIni["objCfg"].has_option('ADHERENTS', 'Adherents_orderBy') and len(dIni["objCfg"]['ADHERENTS']['Adherents_orderBy'].strip()) > 0) :
        Adherents_orderBy = dIni["objCfg"]['ADHERENTS']['Adherents_orderBy'].strip()
    else :
        log("ERREUR : Pour la liste des Adherents, pas de colonne d'ordonnancement dans le fichier de configuration")
        if (dIni['verbose']) :
            print("ERREUR : Pour la liste des Adherents, pas de colonne d'ordonnancement dans le fichier de configuration")
        exit()
        
    if (dIni["objCfg"].has_option('ADHERENTS', 'Adherents_fichierListe') and len(dIni["objCfg"]['ADHERENTS']['Adherents_fichierListe'].strip()) > 0) :
        Adherents_fichierListe = dIni["objCfg"]['ADHERENTS']['Adherents_fichierListe'].strip()
    else :
        log("ERREUR : Pour la liste des Adherents, pas de fichier dans le fichier de configuration")
        if (dIni['verbose']) :
            print("ERREUR : Pour la liste des Adherents, pas de fichier dans le fichier de configuration")
        exit()
        
    # Test de la presence du fichier liste Adherents
    if (not os.path.exists(Adherents_fichierListe)) :
        log("ERROR : Pour la liste des Adherents, le fichier [" + Adherents_fichierListe + "] est introuvable")
        exit()
    
    # Lecture du fichier (Les EOL sont presents !)
    try :
        with open(Adherents_fichierListe, "rt") as fAdherents :
            lAdherents_fichier = fAdherents.readlines()
    except : 
        log("ERREUR : pb lecture fichier [" + Adherents_fichierListe + "]")
        if (dIni['verbose']) : 
            print("ERREUR : pb lecture fichier [" + Adherents_fichierListe + "]")
    ##  Constituer la liste des Adherents dans un format attendu par la GUI
    # Quel est l'indice de la colonne de tri ?
    # TODO le separateur dans le fichier de config !
    ligne = lAdherents_fichier[0].strip().split("\t")
    # TODO si l'indice n'est pas trouve, alors ValueError
    Adherents_orderBy_index = ligne.index(Adherents_orderBy)
    dAdherents_gui = dict()
    dAdherents     = dict()
    # Suppression de l'entete (elle est dans la variable ligne)
    del lAdherents_fichier[0]
    for l in lAdherents_fichier : 
        l = l.strip("\n")
        #print("l=" + l)
        adherent_infos = l.split("\t")
        if (len(adherent_infos[0]) > 0) : 
            dAdh_gui = dict()
            dAdh     = dict()
            #print("Adh=" + adherent_infos[0])
            dAdh_gui['adhId'] = adherent_infos[0]
            if (len(adherent_infos[2]) > 0) : 
                dAdh_gui['lbl_btn'] = adherent_infos[0] + " - " + adherent_infos[2] + "\n" + adherent_infos[1]
                #dAdherents_gui[adherent_infos[Adherents_orderBy_index]] = adherent_infos[0] + " - " + adherent_infos[2] + "\n" + adherent_infos[1]
            else : 
                dAdh_gui['lbl_btn'] = adherent_infos[0] + "\n" + adherent_infos[1]
                #dAdherents_gui[adherent_infos[Adherents_orderBy_index]] = adherent_infos[0] + "\n" + adherent_infos[1]
            ##  Les headers sur le ligne 1
            #for i in range(3, len(ligne)) : 
            for i, h in enumerate(ligne) : 
                # i contient l'indice de la colonne, h contient le contenu (header)
                #dAdh[ligne[i]] = adherent_infos[i]
                dAdh[h] = adherent_infos[i]
                #print("i=", i, ", h=", h, ", val=", dAdh[h])
            
            dAdherents_gui[adherent_infos[Adherents_orderBy_index]] = dAdh_gui
            dAdherents[adherent_infos[0]] = dAdh
        else : 
            dAdherents_gui[adherent_infos[Adherents_orderBy_index]] = None
    
    #print("len=" + str(len(dAdherents_gui)))
    # print("\ndAherent_gui\n")
    # print(dAdherents_gui)
    # print("\n")
    
    dIni['dAdherents_gui'] = dAdherents_gui
    dIni['dAdherents'] = dAdherents
    
    
def getInifile() : 
    """ Recuperer le fichier de configuration,
    le stocker dans la structure dIni
    """
    global Verbose
    cfg = configparser.ConfigParser()
    cfg.read(dIni['iniFile'])  
    dIni["objCfg"] = cfg
    log("INFO : fichier de configuration lu")
    
    ##   Niveau de verbose
    if (cfg.has_option('GENERAL', 'verbose') and len(cfg['GENERAL']['verbose'].strip()) > 0) :
        Verbose = dIni['verbose'] = myStr2bool(cfg['GENERAL']['verbose'].strip())


def getCmdline() :
    """ Analyser la ligne de commande
    On attend --ini ou --cfg avec le nom du fichier de configuration,
    sinon, le nom du script, suffixé par .ini ou .cfg
    """
    cfgFileExtRequired = ('.ini', '.cfg')
    (cfgFilePath, cfgFileName) = os.path.split(sys.argv[0])
    (cfgFileNameShort, cfgFileNameExt) = os.path.splitext(cfgFileName)
    
    dIni['cmdLine'] = " ".join(sys.argv)
    log("INFO : " + dIni['cmdLine'])
    parser = argparse.ArgumentParser()
    #parser.add_argument("-c", "--cfg",          required = True, dest='cfgFile',        help="Le fichier de configuration est obligatoire") # , default=cfgFileFullName
    parser.add_argument("-c", "--cfg", dest='cfgFile', default=None, help="Le nom du fichier de configuration.cfg")
    parser.add_argument("-i", "--ini", dest='iniFile', default=None, help="Le nom du fichier de configuration.ini")
    args = parser.parse_args()

    if (not args.cfgFile and not args.iniFile) :
        #not os.path.exists(args.cfgFile) and not os.path.exists(args.iniFile)): 
        log("INFO : Fichier configuration non fourni")
        for ext in cfgFileExtRequired :
            cfgFileFullName = os.path.join(cfgFilePath, cfgFileNameShort) + ext
            if (os.path.exists(cfgFileFullName)) :
                dIni['iniFile'] = cfgFileFullName
                break
        if (not 'iniFile' in dIni) :
            log("ERROR : Configuration : Fichier de configuration PAR DEFAUT [" + cfgFileNameShort+ "] (.ini ou .cfg) introuvable")
            exit(2)
    else :
        if (args.iniFile) :
            dIni['iniFile'] = args.iniFile
        else : 
            dIni['iniFile'] = args.cfgFile
        # Test de la presence du fichier ini
        if (not os.path.exists(dIni['iniFile'])) :
            log("ERROR : Configuration : Fichier de configuration FOURNI [" + cfgFileNameShort+ "] (.ini ou .cfg) introuvable")
            exit(1)
    return

    
def alert(p) :
    """ Je ne sers pas a grand chose
    """
    showinfo("Alerte", p)

    
def log(s) :
    """ Ecrire sur la sortie des erreurs
    """
    print(str(s), file=sys.stderr)
    return True

    
def pointeuse() :
    """ Retourne un horodatage
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
def myStr2bool(v):
    """ Retourne True ou False suivant une valeur de type String
    """
    return v.lower() in ("yes", "true", "y", "t", "1", "oui", "o")
    
    
if __name__ == '__main__':
    print("Je suis le module principal d'une application, pas une application")