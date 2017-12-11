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


def secDictJobObjectVersion(f) :
    '''
    Le parametre est un fichier (separateur TAB)
    Format du fichier ==    Object_Target_Code<TAB>Object_Target_Alias_Name<TAB>Flux_Version<TAB>Job_Version
                            W300050	PRFL_MABQE_QUOTD	E28_0	E28_0
    Cette fonction retourne un dictionnaire 
        clef   == Object_Target_Alias_Name + "_" + Flux_Version (ce qui forme le nom du job
        valeur == liste(Object_Target_Code, Flux_Version[, Job_Version]
    '''
    try :
        fJov = open(f, 'r')
    except IOError as e:
        print("Le fichier dictionnaire [" + f + "] ne peut etre ouvert !")
        print("except ({0}) : {1}".format(e.errno, e.strerror))
        quit()
    except :
        print("Le fichier dictionnaire [" + f + "] ne peut etre ouvert !")
        print("erreur : " + str(sys.exc_info()[0]))
        quit()
    dJov = dVer = dict()
    for line in fJov.readlines() :
        lValues = line.split(TAB)
        if (lValues[0] and lValues[1] and lValues[2]) :
            obj = lValues[0]
            job = lValues[1]
            ver = lValues[2]
            dJov[job + "_" + ver] = obj
            dJov[job] = obj
            # Un SET serait plus pythonic, mais peut-etre moins comprehensible
            dVer[ver] = ver
    fJov.close()
    
    return (dJov, dVer)
    

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
dsjobEnrichissementNumber = 0
dsjobWoErrCode = dsjobWoErrDesc = dsjobWoErr = 0
initializeNumber = mainloopNumber = 0
initializeEquilibre = mainloopEquilibre = 0
intervarNumber = ifNumber = intervarSsIfNumber = 0
errCodeNumber = errDescNumber = 0
nbrMaxMainloop = nbrMaxErrCode = nbrMaxErrDesc = 0
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
bShowJobGreater2 = os.getenv("dsXshowJobGreater2", False)
bShowJobEnrichissement = os.getenv("dsXshowJobEnrichissement", False)
bShowSynthese = os.getenv("dsXsynthese", False)

bIf = False

##  Prise en compte des ObjectCodeTo
##  dsXjobObjectVersionFile
# Object_Target_Code	Object_Target_Alias_Name	Flux_Version	Job_Version
# W30336B	TYP_MTF_ENTREE_DFT_CST	1002	1002
# W300050	PRFL_MABQE_QUOTD	E28_0	E28_0
sJobObjectVersionFilename = os.getenv("dsXjobObjectVersionFile", False)
if (not sJobObjectVersionFilename) :
    print("env var attendue : dsXjobObjectVersionFile suivi du chemin complet du fichier object / job / version")
    quit()
if (not os.path.exists(sJobObjectVersionFilename)) :
    print("Fichier", sJobObjectVersionFilename, "introuvable")
    quit()
(dJobObjectVersion, dVersion) = secDictJobObjectVersion(sJobObjectVersionFilename)


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
            dIntervar = dict()
            nbrMaxMainloopTmp = nbrMaxErrCodeTmp = nbrMaxErrDescTmp = 0
            continue

        if (line[0:9] == "END DSJOB") :
            bDsjobHeader = False
            bDsjob = False
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
            #
            # Nombre max de mainloop / ErrCode / ErrDesc par job
            nbrMaxMainloop = max(nbrMaxMainloop, nbrMaxMainloopTmp)
            nbrMaxErrCode = max(nbrMaxErrCode, nbrMaxErrCodeTmp)
            nbrMaxErrDesc = max(nbrMaxErrDesc, nbrMaxErrDescTmp)
            dDsx[dsjobIdentifier]["nbrMaxMainloop"] = nbrMaxMainloopTmp
            dDsx[dsjobIdentifier]["nbrMaxErrCode"] = nbrMaxErrCodeTmp
            dDsx[dsjobIdentifier]["nbrMaxErrDesc"] = nbrMaxErrDescTmp
            if (bShowAll and bShowJobGreater2 and (nbrMaxMainloopTmp > 1 or nbrMaxErrCodeTmp > 1 or nbrMaxErrDescTmp > 1)) :
                print(lineNumber, "Pour ce job ", dsjobIdentifier, ":", nbrMaxMainloopTmp, "mainloop,", nbrMaxErrCodeTmp, "ERR_Code,", nbrMaxErrDescTmp, "Err_Desc")
                if(dsjobNameVersion and nbrMaxMainloopTmp > 1 and (nbrMaxErrCodeTmp > 0 or nbrMaxErrDescTmp > 0) ) :
                    print("! ! ! Job enrichissement avec plusieurs mainloop ET des ERR_ ! ! !")
                    # Jx_S_DTA_WRK_Enrichissement_CRED_SOFINCO_A_E25_2 
                    # Jx_S_DTA_WRK_Enrichissement_CRED_SOFINCO_B_E25_2
                if(dsjobNameVersion and (nbrMaxErrCodeTmp != nbrMaxErrDescTmp)) :
                    print("! ! ! Job enrichissement avec nbr ERR_ differents ! ! !")
                    # 0
                if(not nbrMaxErrCodeTmp == nbrMaxErrDescTmp) :
                    print("! ! ! Job NON enrichissement avec nbr ERR_ differents ! ! !")
                    # 0
                
            if (dDsx[dsjobIdentifier]['dsjobIdentifier'] == bShowThisJob) :
                bShowAll = False
            continue

            line.replace("\\(9)", " ").replace("\t", " ")
        if (bDsjobHeader and line[0:13]  == "   Identifier") :
            lTmp = line.split('"')
            dsjobIdentifier = lTmp[1]
            dDsx[dsjobIdentifier] = dict()
            dDsx[dsjobIdentifier]['dsjobIdentifier'] = dsjobIdentifier
            
            ## Est-ce bien un job d'enrichissement ?
            ##  Jx_S_DTA_WRK_Enrichissement_
            ##  Jx_Sn_DTA_WRK_Enrichissement_
            dsjobNameVersion = False
            if (dsjobIdentifier[0:28].upper() == "JX_S_DTA_WRK_ENRICHISSEMENT_") :
                dsjobNameVersion = dsjobIdentifier[28:]
            if (dsjobIdentifier[0:29].upper() == "JX_SN_DTA_WRK_ENRICHISSEMENT_") :
                dsjobNameVersion = dsjobIdentifier[29:]
            dDsx[dsjobIdentifier]['dsjobEnrichissement'] = dsjobNameVersion
            if (dsjobNameVersion) :
                dsjobEnrichissementNumber += 1            
            dDsx[dsjobIdentifier]['dsjobName'] = False
            dDsx[dsjobIdentifier]['dsjobVersion'] = False
            dDsx[dsjobIdentifier]['dsjobPlanif'] = False
            if (dsjobNameVersion) :
                lTmp = dsjobNameVersion.rsplit('_', 2)
                #print(TAB, "----- lTmp[0]", lTmp[0], "lTmp[1]", lTmp[1], "lTmp[2]", lTmp[2])
                if (lTmp[2].isdigit()) :
                    #print(TAB, "int(lTmp[2])", int(lTmp[2]))
                    if (int(lTmp[2]) > 100 and int(lTmp[2]) < 10000) :
                        dsjobVersion = lTmp[2]
                        #print(TAB, "dsjobVersion INT =", dsjobVersion)
                        # Jx_S_DTA_WRK_Enrichissement_A_BDF_MENS_1002
                        # lTmp[0]==A_BDF lTmp[1]==MENS lTmp[2]==1002
                        dsjobName = lTmp[0] + "_" + lTmp[1]
                    else :
                        if (lTmp[1].isdigit() and int(lTmp[1]) < 100) : 
                            dsjobVersion = lTmp[1] + "_" + lTmp[2]
                            #print(TAB, "dsjobVersion INT_INT =", dsjobVersion)
                        else :
                            if (lTmp[1][0:1].isalpha() and lTmp[1][1:].isdigit() and int(lTmp[1][1:]) < 100) :
                                dsjobVersion = lTmp[1] + "_" + lTmp[2]
                                #print(TAB, "dsjobVersion XINT_INT =", dsjobVersion)
                            #else :
                                #pass
                                #print(TAB, "???")
                        dsjobName = lTmp[0]
                #print(TAB, "dsjobName :", dsjobName, TAB, "dsjobVersion :", dsjobVersion)
                dDsx[dsjobIdentifier]['dsjobName'] = dsjobName
                dDsx[dsjobIdentifier]['dsjobVersion'] = dsjobVersion
                ## Controle que la version existe bien, sinon, pas valide !
                if (dsjobNameVersion in dJobObjectVersion) : 
                    dDsx[dsjobIdentifier]['dsjobPlanif'] = True
            
            identifierNumber += 1
            if (bShowThisJob == dsjobIdentifier) :
                #print("Celui ci ! [" + dsjobIdentifier + "]")
                bShowAll = True
            if (bShowAll and bShowIdentifier) :
                print("- - - - - - -")
                print(lineNumber, "dsjobIdentifier :", dsjobIdentifier) 
                if (bShowJobEnrichissement and dsjobNameVersion) :
                    print(lineNumber, dsjobIdentifier, "est un job d'enrichissement")
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
            nbrMaxMainloopTmp += 1 
            if (bShowAll and bShowStructure) :
                print(lineNumber, "mainloop :") 
            continue

        if (bMainloop and line[0:8] == 'finish {') :
            bMainloop = False
            bFinish = True
            mainloopEquilibre -= 1
            if (bShowAll and bShowStructure) :
                print(lineNumber, "finish :") 
            continue

        # Ne prendre que les InterVar dans un bloc if, pas dans un bloc else
        # [ if (StageVar0_svReject1)]
        # Chaque couple ERR_Code / ERR_Desc a son bloc if (
        line = line.replace('\\(9)', "").strip()
        if (line.find("if (") > -1) :
            bIf = True
            ifNumber += 1
            ifBloc = line.replace(" ", "").replace("if(", "").replace(")", "")
            #print("ifBloc :", ifBloc)
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
            nbrMaxErrCodeTmp += 1
            (retCode, l) = detectErrOtherIntervar(line)
            if (not retCode) : 
                print(lineNumber, "Pb:", "+".join(l))
            if (bShowAll and bShowErrCode) :
                print(lineNumber, "ERR_Code :", line.strip(), TAB, " ifBloc :", ifBloc) 
            continue
            
        if (bMainloop and posErrDesc > 0 and posErrDesc < posEqual) : 
            bErrDesc = True
            errDescNumber += 1
            nbrMaxErrDescTmp += 1
            (retCode, l) = detectErrOtherIntervar(line)
            if (not retCode) : 
                print(lineNumber, "Pb:", "+".join(l))
            if (bShowAll and bShowErrDescription) :
                print(lineNumber, "ERR_Desc :", line.strip(), TAB, " ifBloc :", ifBloc) 
            continue
        
        if ((bInitialize or bMainloop) and posInterVar > -1 and posInterVar < posEqual) :
            intervarNumber += 1
            if (bMainloop and not bIf) :
                intervarSsIfNumber += 1
                if (bShowAll and bShowIntervarElse) :
                    print(lineNumber, "Not if InterVar :", line.strip())
            else :
                ##  Intervar est, ou dans le bloc initialize, ou (dans le bloc mainloop ET dans un if)
                # \"V\"
                # \"19000101\"
                # \"%yyyy%mm%dd\"
                # \"*\"
                # \"|\"
                # \"CIR\"
                # \"1\"
                # LN_Done.Row_Found_CIR2a
                # TRANSFORMER_psPrmJxWRK_pObjectCodeTo
                l = line.split("=", 1)
                ### Jamais detectee len(l) != 2 
                k = l[0].strip()
                v = l[1][:-1].strip() # suppression du ; final
                #v = v.replace('\\"', '') # suppression de \"
                v = v.lstrip('\\"').rstrip('\\"') # suppression des \" lateraux
                v = v.replace('\\', '') #suppression des \
                if (v[0:8].upper() == "LN_DONE.") : 
                    v = v[8:]
                if (v[-14:].upper() == "_POBJECTCODETO") : 
                    v = "<ObjectCodeTo>"
                #print("v[-14:] =", v[-14:], TAB, " intervar :", k, TAB, " =", v, TAB, " (", l[1], ")")
                if (v[0:8].upper() == "INTERVAR") :
                    #print("INDIRECTE", line)
                    v = dIntervar[v]
                    if (v[0:8].upper() == "INTERVAR") : ### Jamais detectee !
                        #print("INDIRECTE AGAIN !")
                        v = dIntervar[v]
                #print(TAB, " intervar :", k, TAB, " =", v, TAB, " (", l[1], ")")
                dIntervar[k] = v

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
    print("Nbr jobs enrichiss :", dsjobEnrichissementNumber)
    print("Nombre de IDs      :", identifierNumber)
    print("Nombre initialize  :", initializeNumber)
    print("Equilibre init     :", initializeEquilibre)
    print("Nombre mainloop    :", mainloopNumber)
    print("Equilibre mainloop :", mainloopEquilibre)
    print("Max mainloop / job :", nbrMaxMainloop)
    print("Nombre ERR_Code    :", errCodeNumber)
    print("Max ERR_Code / job :", nbrMaxErrCode)
    print("Nombre ERR_Desc    :", errDescNumber)
    print("Max ERR_Desc / job :", nbrMaxErrDesc)
    print("Nbr IDs ss Err     :", dsjobWoErr)
    print("Nbr IDs ss ErrCode :", dsjobWoErrCode)
    print("Nbr IDs ss ErrDesc :", dsjobWoErrDesc)
    print("Nombre InterVar    :", intervarNumber)
    print("Nbr InterVar ss if :", intervarSsIfNumber)
    print("Nombre de if (     :", ifNumber)

print("")
print("-------------------- dDsx --------------------")
#print(dDsx)

# for (k, v) in enumerate(dDsx) :
    # print(v, ":")
    # for (i) in dDsx[v] :
        # print(TAB, i, "=", dDsx[v][i])
