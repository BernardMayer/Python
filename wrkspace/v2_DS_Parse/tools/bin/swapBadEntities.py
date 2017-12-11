#!/python
# -*- coding: utf-8 -*-
### http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
from __future__ import unicode_literals
from __future__ import print_function

"""
Les modules pyodbc, pathlib, configparser ne sont pas disponibles 
sur nos machines Linux RedHat python 2.6.6
"""

import cgitb
cgitb.enable(format='text')

import sys
import os
#import string
#import pyodbc
#import pathlib
import argparse
#import configparser
import re
#from collections import OrderedDict
import collections
import time
import datetime
import decimal


decimal.getcontext().prec = 2
TAB = '\t'
FileOutSep = TAB
FileOutHeader = False
Verbose = True
dtNow  = datetime.datetime.today()
tsNow = dtNow.timestamp()


## fichier a traiter
me = sys.argv[0]
#args = sys.argv[1:]
if (len(sys.argv) == 1) :
    print("Le fichier pjb dit etre le 1er parametre de " + me, file=sys.stderr)
    quit()
if (len(sys.argv) == 2) :
    pjbFilename = sys.argv[1]
    print("Traitement du fichier pjb " + pjbFilename, file=sys.stderr)

if (not os.path.exists(pjbFilename)) :
    print(pjbFilename + " est introuvable", file=sys.stderr)
    quit()

    
##  Faire l'inventaire des entities
##  https://stackoverflow.com/questions/7693515/why-is-elementtree-raising-a-parseerror
##  https://stackoverflow.com/questions/14744945/parse-xml-with-xhtml-entities
##  Remplace &#x1D; par LF (http://www.asciitable.com/) Dec:10 Hex:A Oct:012


# Ouvrir le fichier, verfier la 1ere ligne
with open(pjbFilename, 'r') as fPjb :
    try :
        line = fPjb.readline()
    except :
        print("Erreur de lecture ou fichier vide de", pjbFilename, file=sys.stderr)
        quit()
    if (line.upper().find("XML VERSION") == -1) :
        print("Ce fichier est-il du XML ?", pjbFilename, file=sys.stderr)
        quit()
    else :
        print(line, end='')
    ## On peut y aller ...
    dEntities = dict()
    #rx = re.compile("&#([0-9]+);|&#x([0-9a-fA-F]+);")
    rx = re.compile("&#[0-9]+;|&#x[0-9a-fA-F]+;")
    nLine = 1
    for line in fPjb.readlines() :
        nLine += 1
        #print(nLine)
        l = rx.findall(line)
        if (not l) :
            print(line, end='')
        else :
            #print(nLine, TAB, "l", TAB, l)
            for e in l :
                if (e in dEntities) :
                    dEntities[e] += 1
                else :
                    dEntities[e] = 1
            print(line.replace("&#x1D;", "&#xA;").replace("&#x1E;", "&#xA;"), end='')
#print(dEntities)
for e in dEntities :
    print(e, TAB, dEntities[e], file=sys.stderr)
