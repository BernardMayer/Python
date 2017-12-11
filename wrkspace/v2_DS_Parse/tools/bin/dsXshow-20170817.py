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

def cleanErrMsg(s) :
    ''' Decape les messages ERR_Code ERR_Description avec vigueur
    ustring_from_string    # LN_Reject_7.ERR_Description = ustring_from_string(InterVar0_10);
    ustring_from_timestamp    # + ustring_from_timestamp(LN_Done.DT_ELIG)) + 
    ustring_from_date    # 9)\(9)\(9)InterVar0_23 = ustring_from_date(LN_Done.DDVAL_INTSPE);
    u_trimc_string    # + u_trimc_string(InterVar0_17 , InterVar0_25)) + #### ! ! ! ! !
    ustring_from_decimal    # + ustring_from_decimal(LN_Done.CPOBJA)
    u_replace_substring #
    u_char_from_num #
    u_left_substring    #
    substring_1 #
    '''
    s = s.replace("ustring_from_string", "").replace("ustring_from_decimal", "")
    s = s.replace("ustring_from_timestamp", "").replace("ustring_from_date", "")
    ##  Conformer les champs de DB
    ##  InterVar0_49+LN_Done.DDVAL+InterVar0_50
    retCode = True
    l = s.split("+")
    for k, v in enumerate(l) :
        if (v[0:8].upper() == "INTERVAR") :
            continue
        if (v[0:8].upper() == "LN_DONE.") : 
            l[k] = v[8:]
            #print("---- i [" + l[k] + "]")
            continue
        ## TRANSFORMER_psPrmJxWRK_pObjectCodeTo;  ? ? ?
        #print("v", v, TAB, "DEBUG", v[-12:])
        if (v[-12:].upper() == "OBJECTCODETO" ) :    
            l[k] = "<ObjectCodeTo>"
            continue
        ## u_trimc_string(InterVar0_21 , InterVar0_25)
        #print("v[0:14]", v[0:14], "v[14:26]", v[14:26])
        if (v[0:14].upper() == "U_TRIMC_STRING") :
            l[k] = v[14:26]
            continue
        ##Dans les autres cas ...
        retCode = False
    s = "+".join(l)    
    #print("DEBUG :", s)
    return retCode, s


def detectErrOtherIntervar(sBrute) :
    ''' Detecter les lignes d'erreurs (ERR_Code et ERR_Description) 
        qui ont d'autres variables que des "InterVar"
        et simplifier les champs de DB
    '''
    # ret = True
    (nul, l) = sBrute.split(" = ")
    # if (l.find("=") > -1) :
        # ret = False
    sOk = l.replace("(", "").replace(")", "").replace(" ", "").replace(";", "") # .replace("+", "")
    sCtrl = sOk.replace("+", "")
    sCtrl = re.sub("InterVar[0-9]+_[0-9]+", "", sCtrl)
    #print("Apres re.sub [" + l + "]") 
    if (len(sCtrl) > 0) :
        #print("avant :", sOk)
        (retCode, sOk) = cleanErrMsg(sOk)
        #print("apres :", sOk)
        if (not retCode) :
            print(nLine, TAB, "Alarme l :", l, "\nsOk :", sOk) 
        #print("retCode :", retCode, TAB, " apres :", sOk)
    else :
        retCode = True
    return retCode, sOk.split("+")

##
##  Declarations / Affectations
##

##  Structure container config
dIni = dict()

decimal.getcontext().prec = 2
TAB = '\t'
FileOutSep = TAB
FileOutHeader = False
Verbose = True
dIni['verbose'] = Verbose
dtNow  = datetime.datetime.today()
tsNow = dtNow.timestamp()

bDsjob = bDsjobHeader = False
bInitialize = bMainloop = False
bErrCode = bErrDesc = 0
nLine = 0
dsjobNumber = identifierNumber = 0
dsjobWoErrCode = dsjobWoErrDesc = dsjobWoErr = 0
initializeNumber = mainloopNumber = 0
initializeEquilibre = mainloopEquilibre = 0
intervarNumber = ifNumber = intervarSsIfNumber = 0
errCodeNumber = errDescNumber = 0
## fichier a traiter
me = sys.argv[0]
#args = sys.argv[1:]
if (len(sys.argv) == 1) :
    print("Le fichier dsx dit etre le 1er parametre de " + me)
    quit()
if (len(sys.argv) == 2) :
    dsxFilename = sys.argv[1]
    print("Traitement du fichier dsx " + dsxFilename)

##
## parametress de fonctionnement
## 
bShowThisJob = os.getenv("dsXthisJob", False)
bShowAll = not bShowThisJob
bShowIdentifier = os.getenv("dsXidentifier", False)
bShowStructure = os.getenv("dsXstructure", False)
bShowIntervar = os.getenv("dsXintervar", False)
bShowIntervarElse = os.getenv("dsXintervarElse", False)
bShowIf = os.getenv("dsXif", False)
bShowErrCode = os.getenv("dsXerrcode", False)
bShowErrDescription = os.getenv("dsXerrdescription", False)
bShowLinenumber = os.getenv("dsXlinenumber", False)
bShowSynthese = os.getenv("dsXsynthese", False)

bIf = False



## Lecture du fichier
dDsx = dict()
if (not os.path.exists(dsxFilename)) :
    print("Fichier", dsxFilename, "introuvable")
    quit()
with open(dsxFilename, 'r') as fDsx :
    for line in fDsx.readlines() :
        nLine += 1
        if (bShowAll and bShowLinenumber) :
            lineNumber = str(nLine) + TAB
        else :
            lineNumber = ""
        if (line[0:11] == "BEGIN DSJOB") :
            bDsjob = True
            bDsjobHeader = True
            dsjobNumber += 1
            continue
        if (line[0:9] == "END DSJOB") :
            bDsjobHeader = False
            bDsjob = False
            
            if (dDsx[dsjobIdentifier]['dsjobIdentifier'] == bShowThisJob) :
                bShowAll = False
            
            
            #
            # Nbr de job sans ERR_Code / ERR_Description
            #dsjobWoErrCode = dsjobWoErrDesc = dsjobWoErr
            if (bErrCode) : 
                dsjobWoErrCode += 1
            if (bErrDesc) :
                dsjobWoErrDesc += 1
            if (bErrCode and bErrDesc) :
                dsjobWoErr += 1
                
            bErrCode = bErrDesc = False
            continue
        line.replace("\\(9)", " ").replace("\t", " ")
        if (bDsjobHeader and line[0:13]  == "   Identifier") :
            lTmp = line.split('"')
            dsjobIdentifier = lTmp[1]
            dDsx[dsjobIdentifier] = dict()
            dDsx[dsjobIdentifier]['dsjobIdentifier'] = dsjobIdentifier
            identifierNumber += 1
            
            if (bShowThisJob == dsjobIdentifier) :
                #print("Celui ci ! [" + dsjobIdentifier + "]")
                bShowAll = True
                
            if (bShowAll and bShowIdentifier) :
                print("- - - - - - -")
                print(lineNumber, "dsjobIdentifier :", dsjobIdentifier) 
            continue
        if (bDsjobHeader and line[0:15]  == "   DateModified") :
            lTmp = line.split('"')
            dsjobModifDate = lTmp[1]
            dDsx[dsjobIdentifier]['dsjobModifDate'] = dsjobModifDate
            continue
        if (bDsjobHeader and line[0:15]  == "   TimeModified") :
            lTmp = line.split('"')
            dsjobModifTime = lTmp[1]
            bDsjobHeader = False
            dDsx[dsjobIdentifier]['dsjobModifTime'] = dsjobModifTime
            #print(dsjobIdentifier, dsjobModifDate, dsjobModifTime)
            continue
        if (bDsjob and not bMainloop and line[0:12] == "initialize {") :
            bDsjobHeader = False
            bInitialize = True
            initializeNumber += 1
            initializeEquilibre += 1
            if (bShowAll and bShowStructure) : 
                print(lineNumber, "init :") 
            continue
        if (bDsjob and bInitialize and not bMainloop and line[0:1] == "}") :
            bInitialize = False
            initializeEquilibre -= 1
            continue
        if (bDsjob and not bInitialize and line[0:10] == 'mainloop {') :
            bInitialize = False
            bMainloop = True
            mainloopNumber += 1
            mainloopEquilibre += 1
            if (bShowAll and bShowStructure) :
                print(lineNumber, "mainloop :") 
            continue
        #if (bDsjob and bMainloop and not bInitialize and line[0:1] == "}") :
            #bMainloop = False
            #continue
        if (bMainloop and line[0:8] == 'finish {') :
            bMainloop = False
            bFinish = True
            mainloopEquilibre -= 1
            if (bShowAll and bShowStructure) :
                print(lineNumber, "finish :") 
            continue
        
        # Ne prendre que les InterVar dans un bloc if, pas dans un bloc else
        # [ if (StageVar0_svReject1)]
        line = line.replace('\\(9)', "").strip()
        if (line.find("if (") > -1) :
            bIf = True
            ifNumber += 1
            if (bShowAll and bShowIf) :
                print(lineNumber, " if () {  ", line)
            continue
        if (bIf and line[0:1] == "}") :
            bIf = False
            if (bShowAll and bShowIf) :
                print(lineNumber, " } /if")
            continue
        
        posErrCode = line.upper().find("ERR_CODE")
        posErrDesc = line.upper().find("ERR_DESCRIPTION")
        posInterVar = line.upper().find("INTERVAR")
        posEqual = line.find(" = ")
        if (bMainloop and posErrCode > 0 and posErrCode < posEqual) : 
            bErrCode = True
            errCodeNumber += 1
            (retCode, l) = detectErrOtherIntervar(line)
            if (not retCode) : 
                print(lineNumber, "Pb:", "+".join(l))
            if (bShowAll and bShowErrCode) :
                print(lineNumber, "ERR_Code :", line.strip()) 
            continue
            
        if (bMainloop and posErrDesc > 0 and posErrDesc < posEqual) : 
            bErrDesc = True
            errDescNumber += 1
            (retCode, l) = detectErrOtherIntervar(line)
            if (not retCode) : 
                print(lineNumber, "Pb:", "+".join(l))
            if (bShowAll and bShowErrDescription) :
                print(lineNumber, "ERR_Desc :", line.strip()) 
            continue
        
        if ((bInitialize or bMainloop) and posInterVar > -1 and posInterVar < posEqual) :
            
            # TODO
            # ! attention au IF ELSE !
            # 192143	 InterVar : InterVar0_19 = LN_Done.IDTAC;
            # 192145	 InterVar : InterVar0_19 = InterVar0_1;            
            
            intervarNumber += 1
            if (bMainloop and not bIf) :
                intervarSsIfNumber += 1
                if (bShowAll and bShowIntervarElse) :
                    print(lineNumber, "Not if InterVar :", line.strip())
            else :
                if (bShowAll and bShowIntervar) :
                    print(lineNumber, "InterVar :", line.strip())                
'''
BEGIN DSJOB
   Identifier "CopyOfJx_S_DTA_WRK_Enrichissement_COUT_RISQ_CRED_MENS_E28_0"
   DateModified "2017-01-10"
   TimeModified "18.42.46"
'''           
if (bShowSynthese) :
    print("")            
    print("-------------------- Synthese --------------------")
    print("Nombre de jobs     :", dsjobNumber)            
    print("Nombre de IDs      :", identifierNumber)
    print("Nombre initialize  :", initializeNumber)
    print("Equilibre init     :", initializeEquilibre)
    print("Nombre mainloop    :", mainloopNumber)
    print("Equilibre mainloop :", mainloopEquilibre)
    print("Nombre ERR_Code    :", errCodeNumber)
    print("Nombre ERR_Desc    :", errDescNumber)
    print("Nbr IDs ss Err     :", dsjobWoErr)
    print("Nbr IDs ss ErrCode :", dsjobWoErrCode)
    print("Nbr IDs ss ErrDesc :", dsjobWoErrDesc)
    print("Nombre InterVar    :", intervarNumber)
    print("Nbr InterVar ss if :", intervarSsIfNumber)
    print("Nombre de if (     :", ifNumber)
