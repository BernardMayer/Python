#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys, re
import subprocess


"""
Utiliser (requeter) la base de donnees
Tant en python 2.6.6 qu'en 3.n
Tant sous linux que sous windows
--> usage de BTEQ ?
"""

"""
http://python-simple.com/python-modules-autres/lancement-process.php
https://stackoverflow.com/questions/5631624/how-to-get-exit-code-when-using-python-subprocess-communicate-method
"""

# Diff Python2 vs python3
# https://python.doctor/page-syntaxe-differente-python2-python3-python-differences

# Pour que les print() fonctionnent
# en python2 (serveurs datastage) ET en python3 (poste de travail)
# print "\n".join([x, y])         -->   print(x, y, sep="\n")
# print >> sys.stderr, "erreur"   -->   print("Erreur", file=sys.stderr)
# print "une ligne ",             -->   print("une ligne", end="")


## Les fonctions sont definies AVANT



##  Methode 1 : Tout est dans un fichier bteq
##  Eventuellement, le fichier est mis a jour avant par un systeme de template

lBteq = list()
lBteq.append('.logon zuy10-d1tda.yres.ytech/ETA2002,ETA2002' + '\n')
# lBteq.append('.logon zuy10-d1tda.yres.ytech/ETA2002' + '\n')
lBteq.append('select 1;' + "\n")
lBteq.append('.logoff' + "\n")
lBteq.append('.quit 88' + "\n")


fdBteq = open("/home/ETA2458/bin/testBteq-KO.bteq", 'r')
lBteq = fdBteq.readlines()
fdBteq.close()

myPopen = subprocess.Popen(
    ['bteq']
    , stdin = subprocess.PIPE
    , stdout = subprocess.PIPE
    , stderr = subprocess.PIPE
    # , encoding = 'utf8'
    )
# myPopen.stdin.write('ligne1\nligne2\nligne3\n')
# myPopen.stdin.write('< C:\\AncienDisqueD\\RepoS\\Python\\wrkspace\\runOs\\bteqrunMini-OK.bteq')
# myPopen.stdin.write('.logon zuy10-d1tda.yres.ytech/ETA2002,ETA2002' + '\n')
# Ouverture d'une fenetre popup pour renseigner le MdP si MdP pas fourni
# myPopen.stdin.write('.logon zuy10-d1tda.yres.ytech/ETA2002' + '\n')
# myPopen.stdin.write('select 1;' + "\n")
# myPopen.stdin.write('.logoff' + "\n")
# myPopen.stdin.write('.quit 88' + "\n")
for l in lBteq :
    myPopen.stdin.write(l)
myPopen.stdin.close()
while True:
    status = myPopen.poll()
    if status is not None:
        break

for line in myPopen.stdout:
    sys.stdout.write(line)
print(status)
