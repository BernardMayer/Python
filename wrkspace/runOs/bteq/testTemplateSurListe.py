#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys, re
from string import Template


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


/data/ZUDA0/Procparm/DTWH/CMN/GEN/cfg/CMN_GEN_Profile_ZUDA0.cfg
# CMN_GEN_Env.cfg
/data/ZUDA0/Procparm/DTWH/CMN/GEN/shl/CMN_GEN_FonctionsTeradata.sh

init_teradata TDALIM

CMN_GEN_TDALIM=CO_ZUDA0DTWH_TERA
CMN_GEN_TDP=zuy10-d1tda.yres.ytech
CMN_GEN_TDSTAT=CO_ZUDA0DTWH_STAT
CMN_GEN_TD_ACCT=
CMN_GEN_TD_LOGON=
CMN_GEN_TD_USER=CO_ZUDA0DTWH_SLUD
C

# Environnement
# . ${CMN_GEN_ENV} 

# Variables liées à l'environnement RCP_LET
. ${RCP_LET_APPLI}/cfg/RCP_LET_Env.cfg

# Fonctions
. ${CMN_GEN_SHL}/CMN_GEN_Fonctions.sh
. ${CMN_GEN_SHL}/CMN_GEN_FonctionsTrace.sh
. ${CMN_GEN_SHL}/CMN_GEN_FonctionsTeradata.sh




lBteqBefore = list()
lBteqBefore.append('.logon zuy10-d1tda.yres.ytech/ETA2002,ETA2002' + '\n')
# lBteqBefore.append('.logon zuy10-d1tda.yres.ytech/ETA2002' + '\n')
lBteqBefore.append('select 1;' + "\n")
lBteqBefore.append('.logoff' + "\n")
lBteqBefore.append('.quit 88' + "\n")

lBteqBefore.append("azerty${a}uiop")

toto = "azerty${a}uiop"
s = Template(toto)
d = dict(a="1234567890", b="dzudb0")
s = s.safe_substitute(d)
# print(s)

lBteq = list()
for l in lBteqBefore :
    s = Template(l)
    lBteq.append( s.safe_substitute(d))
print(lBteq)
