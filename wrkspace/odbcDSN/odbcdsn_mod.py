#!/usr/bin/env python
# encoding: utf-8
"""
odbcdsn_mod.py
"""

import pyodbc
import sys
import os
import argparse
import configparser
import re
#from collections import OrderedDict
import collections
import datetime

from constants import *

def read_ini_infos(ini) :
    global TDAbase
    #DSNuser = DSNuser.upper().split()
    TDAbase = TDAbase.upper().split()
    return ini

def forgeCnxString() :
    ## DSN=MUP10;UID=ETH0589MUP10;PWD=ETH0589MUP10
    return "DSN=" + DSNname.strip() + ";UID=" + DSNuser.strip() + ";PWD=" + DSNpwd.strip()
    
def myStr2bool(v):
    if (v.lower() in ("yes", "true", "y", "t", "1", "oui", "o")) : 
        return True
    else :
        return False

def fichierOuvrir(f, rw = 'r') :
    ### Ouverture du fichier
    try:
        objFichier = open(f, rw) # , encoding="utf8"
        if (VERBOSE) : print("Fichier ouvert [" + f + "]")
    except Exception as e:
        log("ERROR : Une erreur est survenue sur " + f + " --> {} ".format(e))
        exit()
    return objFichier

def log(s) :
    print(str(s), file=sys.stderr)
    return True


def pointeuse() :
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")