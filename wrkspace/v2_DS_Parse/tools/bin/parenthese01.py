#!/python
# -*- coding: utf-8 -*-
### http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
from __future__ import unicode_literals

"""
Les modules pyodbc, pathlib, configparser ne sont pas disponibles 
sur nos machines Linux RedHat python 2.6.6
"""

import cgitb
cgitb.enable(format='text')
import pyodbc
import sys
import os
#import string
import pathlib
import argparse
import configparser
import re
#from collections import OrderedDict
import collections
import time
import datetime
import decimal
decimal.getcontext().prec = 2
try :
    import xml.etree.cElementTree as ET
    print("usage de cElementTree", file=sys.stderr)
except :
    import xml.etree.ElementTree as ET
    print("usage de ElementTree", file=sys.stderr)

dtNow  = datetime.datetime.today()
tsNow = dtNow.timestamp()
TAB = "\t"


## fichier a traiter
me = sys.argv[0]
#args = sys.argv[1:]
if (len(sys.argv) == 1) :
    print("Le fichier doit etre le 1er parametre de [" + me + "]")
    quit()
if (len(sys.argv) == 2) :
    parentheseFilenameFull = sys.argv[1]
    if (os.path.isfile(parentheseFilenameFull) and os.access(parentheseFilenameFull, os.R_OK)) : 
        print("Traitement du fichier [" + parentheseFilenameFull + "]")
    else :
        print("! Le fichier [" + parentheseFilenameFull + "] est introuvable / inacessible")
        exit()

with open(parentheseFilenameFull, 'r') as pFile :
	#sql = pFile.readlines()
	sql = pFile.read()
# print(sql)
# print("\n")

sortie = ""
pile = 0
# debut = fin = 0
# listeCouples = list()
longueur = len(sql)
for i in range(longueur) :
	x = sql[i]
	if (x == "(") :
		#debut = i
		pile += 1
	if (x == ")") :
		#fin = i
		pile -= 1
		#listeCouples.append((debut, fin))
	if (pile == 0 and x != ")") :
		sortie += x
	
print(sql, "\n")
print(sortie)
    # with open(parentheseFilenameFull) as pFile :
        # pass
        # print("ouvert !")
# except IOError as e:
    # print("! Ouverture de [" + parentheseFilenameFull + "] impossible") #Does not exist OR no read permissions
    # exit()
