#!/usr/bin/env python
# encoding: utf-8
"""
odbcdsn.py
"""

from odbc_mod import *

top = pointeuse()
pid = str(os.getpid())
log("--- \nINFO : Top depart : [" + top + "] avec le PID [" + pid + "]")
print("--- \nTop depart : [" + top + "] avec le PID [" + pid + "]")


##  TODO : Verifier les infos OBLIGATOIRES
##  - DSNname, DSNuser, DSNpwd, DTAbase


ini = dict()
ini = read_ini_infos(ini)