#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys, re
# Lecture ds fichiers XL
import xlrd

##  Ne pas prendre en compte la 1ere ligne
ligneStart = 2
##  Eventuellement, s'arreter avant la fin...
ligneStop = None
##  Liste des types d'alim attendus (infoTypeAlimData)
lInfoTypeAlimData = ('AD1', 'AD3', 'AD4', 'AD4.2', 'SERV', 'TAD', u'Hors Périmètre')
lInfoTypeAlimDataTpt = ('AD1', 'AD3', 'AD4', 'AD4.2')
##  regex de conformite de PCL
rePcl = re.compile('^Z[A-Z0-9]{5}$')

"""
Controler le fichier XL qui sert de referentiel CdP (pas le mapping)

<nom de l'outil> <nom du fichier a controler>

Necessite un fichier qui decrit la correspondance entre 
le numero d'ordre de la colonne dans le fichier XL (a partir de 1)
suivi d'une TABULATION
le nom de la variable dans l'outil de controle
car la forme du fichier XL peut changer (ajout/retrait/renommage de colonnes)
Ce fichier porte le meme nom que l'outil, avec l'extension .normalize
"""

# Diff Python2 vs python3
# https://python.doctor/page-syntaxe-differente-python2-python3-python-differences

# Pour que les print() fonctionnent
# en python2 (serveurs datastage) ET en python3 (poste de travail)
# print "\n".join([x, y])         -->   print(x, y, sep="\n")
# print >> sys.stderr, "erreur"   -->   print("Erreur", file=sys.stderr)
# print "une ligne ",             -->   print("une ligne", end="")

def getXLfileName() :
    # Par defaut, on admet que l'onglet est le premier...
    onglet = "1"
    if (len(sys.argv) == 1) :
        print("Indiquer le fichier a controler comme 1er parametre [nom de l'onglet (ou num >= 1)].")
        print("    " + sys.argv[0] + " <chemin et nom du fichier a controler>")
        sys.exit()
    else :
        fileName = sys.argv[1]
        if (not (os.path.exists(fileName) and os.access(fileName, os.R_OK))) :
            print("Le fichier [" + fileName + "] est absent ou illisible")
            sys.exit()
        else :
            if (len(sys.argv) == 3) :
                onglet = sys.argv[2]
            return (fileName, onglet)

def getNormFilename(f, newExtension = ".normalize") :
    # Remplacement de l'extension du ficher par .normalize
    filename_w_ext = os.path.basename(f)
    (filename, file_extension) = os.path.splitext(filename_w_ext)
    # pythonnerie !
    # Comme la fonction renvoit vers une structure de 2 elements,
    # le premier split s'arrete car il n'y a plus d'element a alimenter ;-)
    filename = filename + newExtension
    if (os.path.exists(filename) and os.access(filename, os.R_OK)) :
        return filename
    else :
        print("Le fichier [" + filename + "] est introuvable")
        sys.exit()

def setGlobalNormVars(f, di, dv) :
    # f est le fichier .normalize
    # di et dv sont 2 dict pour trouver le nom par l'index et l'index par le nom
    try :
        fdNorm = open(f, 'r')
        for l in fdNorm :
            # Si le 1er caract de la ligne n'est pas un chiffre
            if (not l[0].isdigit()) :
                continue
            # split sur la tabulation (UNE ET UNE SEULE !)
            # par secu, j'ajoute une tabulation en bout de ligne
            l = l + "\t"
            (i, v, aVirer) = l.split("\t")
            if (not (i.isdigit() and int(i) > 0)) :
                continue
            # Supprimer \n
            v = v.strip()
            di[i] = v
            dv[v] = i
            # Vraiment pas elegant... :-()
            # https://www.programiz.com/python-programming/methods/built-in/globals
            # declaration d'une variable GLOBALE
            # print("[" + i + "]\t[" + v + "]")    
            globals()[v] = None
        fdNorm.close()
        return len(di)
    except e:
        # return False
        print("Erreur lors de la digestion du fichier de normalisation")
        sys.exit()

def ctrl_Ligne(lC, numLigne) :
    ##  Controler la liste de cellule (une ligne)
    for k in lCols :
        # Quelle nom de variable associe a ce numero de col ?
        n = dNormIndex4Var[k]
        # Affecter la valeur de la colonne dans SA variable
        globals()[n] = lC[int(k) - 1]
    # print(lC[0], cdpObjName)
    
    # Le nom de l'objet est renseigne ?
    if (not ctrlNonVide(cdpObjName)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['cdpObjName'] + " \t Nom objet non renseigne")
    # Le libelle de l'objet est renseigne ?
    if (not ctrlNonVide(cdpObjNameLib)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['cdpObjNameLib'] + " \t Libelle objet non renseigne")
    #  Nom du flux est renseigne ?
    if (not ctrlNonVide(infoFluxName)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['infoFluxName'] + " \t Nom du flux non renseigne")
    #  Bloc appli est renseigne ?
    if (not ctrlNonVide(infoBlocAppli)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['infoBlocAppli'] + " \t Bloc appli non renseigne")
    #  Libelle bloc appli  est renseigne ?
    if (not ctrlNonVide(infoBlocAppliLib)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['infoBlocAppliLib'] + " \t Libelle bloc appli non renseigne")
    #  Flux adherent est renseigne ?
    if (not ctrlNonVide(infoFluxAdhCmn)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['infoFluxAdhCmn'] + " \t Flux adherent non renseigne")
    #  Squad support est renseigne ?
    if (not ctrlNonVide(infoSquadSupport)) :
        print("ligne " + str(numLigne + 1) + ":\t col " + dNormVar4Index['infoSquadSupport'] + " \t Squad support non renseigne")
    
    # Le type d'alim est-il conforme ?
    if (not ctrlAlimDataConforme(infoTypeAlimData)) :
        tmp = dNormVar4Index['infoTypeAlimData']
        print("ligne " + str(numLigne + 1) + ":\t col " + tmp + " \t Type d'alim inconnu [" + infoTypeAlimData + "]")
    
    # Un des 3 PCL de plan est conforme ?
    if (not (crtlEstPcl(planPclMef1) or crtlEstPcl(planPclMef2) or crtlEstPcl(planPclTpt))) : 
        tmp = dNormVar4Index['planPclMef1'] + ", " + dNormVar4Index['planPclMef2'] + ", et " + dNormVar4Index['planPclTpt']
        print("ligne " + str(numLigne + 1) + ":\t col " + tmp + " \t Aucun PCL ou PCL mal forme [" + planPclMef1 + "][" + planPclMef2 + "][" + planPclTpt + "]")
        
    # Le PCL TPT est bien associe avec type d'alim ?
    if (not ctrlAlimDataConformTpt(infoTypeAlimData, planPclTpt)) :
        tmp = dNormVar4Index['infoTypeAlimData'] + " et " + dNormVar4Index['planPclTpt']
        print("ligne " + str(numLigne + 1) + ":\t col " + tmp + " \t Type d'alim [" + infoTypeAlimData + "] non conforme pour TPT [" + planPclTpt + "]")
              
def ctrlNonVide(s) :
    if (s is None or s == "") :
        return False
    else:    
        return True

def ctrlAlimDataConforme(s) :
    if (not s in lInfoTypeAlimData) :
        return False
    else :
        return True

def crtlEstPcl(s) :
    s = str(s)
    if (s is None or rePcl.match(s) is None) :
        return False
    else :
        return True

def ctrlAlimDataConformTpt(s, pclTpt) :
    if (not s in lInfoTypeAlimDataTpt and not crtlEstPcl(pclTpt)) :
        return False
    else :
        return True



##
##  main()
##    
    
##  Recuperer le nom du fichier a controler et de l'ID de l'onglet
(xlFilename, onglet) = getXLfileName()

##  Deduire le nom du fichier normalize
normFilename = getNormFilename(xlFilename)

##  Prise en compte de la normalisation
##  (Declaration de variables GLOBALES nommees comme dans le fichier)
dNormIndex4Var = dict()
dNormVar4Index = dict()
nbrVarsGlob = setGlobalNormVars(normFilename, dNormIndex4Var, dNormVar4Index)
# print(globals())
##  Construire la liste des colonnes qui nous interessent
lCols = dNormIndex4Var.keys()
# Trier NUMERIQUEMENT
# La liste contient des string ca donne : 1, 11, 12, 2, 3 au lieu de 1, 2, 3, 11, 12
# lCols.sort(key=int) # Ne marche pas a la maison python 3.6
lCOls = sorted(lCols, key=int)

##  Lecture du fichier XL
book = xlrd.open_workbook(xlFilename)
# print(book.sheet_names())
try :
    book = xlrd.open_workbook(xlFilename)
    if (onglet.isdigit()) :
        sheet = book.sheet_by_index(int(onglet) - 1)
    else :
        # TODO : Ouvrir un onglet comportant un accent (pb unicode)
        # session DOS chcp 850 ou CHCP 65001
        sheet = book.sheet_by_name(onglet)
except xlrd.XLRDError as e :
    # XLRDError
    print("Erreur avec le fichier XL (nom onglet inexistant ?)", "\n", e.message)
    sys.exit()
except IndexError as e :
    # XLRDError
    print("Erreur avec le fichier XL (index onglet inexistant ?)", "\n", e.message)
    sys.exit()
    
# print("num_rows =", sheet.nrows)

num_rows = sheet.nrows
# La numerotation des lignes commence a 0, alors qu'XL affiche 1...
curr_row = ligneStart - 1
while curr_row < num_rows:
  row = sheet.row(curr_row)
  lCells = sheet.row_values(curr_row)
  # print('Row:', curr_row, sheet.row_values(curr_row))
  # fdTgt.write(sep.join(lCells) + "\n")
  retCode = ctrl_Ligne(lCells, curr_row)
  if (ligneStop is not None and curr_row >= ligneStop) :
    break
  ##  Ne pas oublier le controle de la boucle :-) 
  curr_row += 1
