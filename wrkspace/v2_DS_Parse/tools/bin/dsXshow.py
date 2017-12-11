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
    dJov = dict()
    dVer = dict()
    dSrc = dict()
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
            try :
                dSrc[job + "_" + ver] = lValues[5] + TAB + lValues[4] 
            except :
                dSrc[job + "_" + ver] = False
    fJov.close()
    #print(dJov)
    # print(dVer)
    # print(dSrc)
    #quit()
    return (dJov, dVer, dSrc)


    
def replaceIntervarByValues(li, di, dJov, jobName, jobVersion) :
    ''' Remplacer chaque intervar par la valeur connues (si presente) dans le dictionnaire
    (retCode, s) = replaceIntervarByValues(l, dIntervar) 
    '''
    ret = False
    s = ""
    if (jobName and jobVersion) :
        jobNameVersion = jobName + "_" + jobVersion
        # has_key
        if (jobNameVersion in dJov) :
            jobCode = dJov[jobNameVersion]
        else :
            jobCode = False
    else :
        jobNameVersion = False
    
    for i in li :
        #if (d.has_key(i)) : # obsolete en python 3
        if (i in di) : 
            #s += di[i] + " " 
            if (jobNameVersion and jobCode and di[i] == "<ObjectCodeTo>") : 
                s += jobCode + " " 
            else :
                isIntervar = (di[i].upper().find("INTERVAR") > -1 and di[i].find("+") > -1)
                if (isIntervar) : 
                    s2 = di[i].replace("(", "").replace(")", "").replace(" ", "")
                    ##  Recursivite !
                    (ret, s2) = replaceIntervarByValues(s2.split("+"), di, dJov, jobName, jobVersion)
                    s += s2 + " "
                else :
                    s += di[i] + " " 
        else :
            s += i + " "
    
    return ret, s
    
    
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
            l[k] = "<" + v[8:] + ">"
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
bDsRecord = bdsrecordName = False
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
bShowRecordName = os.getenv("dsXrecordName", False)
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

bIf = bElse = False

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
(dJobObjectVersion, dVersion, dSource) = secDictJobObjectVersion(sJobObjectVersionFilename)


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
        
        # bDsRecord = bdsrecordName = False
        #    BEGIN DSRECORD
        #       Name "TR_Source"
        #    END DSRECORD
        if (line.strip()[0:14] == "BEGIN DSRECORD") :
            bDsRecord = True
            continue
        if (line.strip()[0:12] == "END DSRECORD") :
            bDsRecord = False
            dsrecordIfBloc = ""
            continue
        if (bDsRecord and line.strip()[0:6] == 'Name "') :
            dsrecordName = line.strip()[6:-1]
            # Faux, mais ; On reste dans le dsRecord, mais on evitera la recherche du nom  ....
            bDsRecord = False
            continue
            
        if (line[0:9] == "END DSJOB") :
            bDsjobHeader = False
            bDsjob = False
            bDsRecord = False
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
            dDsx[dsjobIdentifier]['dsrecords'] = dict()
            #dDsx[dsjobIdentifier]['ifBloc'] = dict()
            
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
            dDsx[dsjobIdentifier]['dsjobSource'] = False
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
                try :
                    dDsx[dsjobIdentifier]['dsjobSource'] = dSource[dsjobNameVersion]
                except : 
                    pass
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
            dDsx[dsjobIdentifier]['dsrecords'][dsrecordName] = dict()
            dDsx[dsjobIdentifier]['dsrecords'][dsrecordName]["name"] = dsrecordName
            dDsx[dsjobIdentifier]['dsrecords'][dsrecordName]["rejets"] = dict()
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
            ifBloc = line.replace(" ", "").replace("if(", "").replace(")", "").replace("(", "")
            if (bShowAll and bShowIf) :
                print(lineNumber, " if () {  ", line)
            continue
        if (line.find("else {") > -1) :
            bElse = True
        if ((bIf or bElse) and line[0:1] == "}") :
            bIf = bElse = False
            if (bShowAll and bShowIf) :
                print(lineNumber, " } /if ou else")
            continue
        
        posErrCode = line.upper().find("ERR_CODE")
        posErrDesc = line.upper().find("ERR_DESCRIPTION")
        posInterVar = line.upper().find("INTERVAR")
        posEqual = line.find(" = ")
        if (bMainloop and posErrCode > 0 and posErrCode < posEqual) : 
            bErrCode = True
            errCodeNumber += 1
            nbrMaxErrCodeTmp += 1
            dsrecordIfBloc = ifBloc
            rejet = line[:posErrCode - 1].strip()
            (retCode, l) = detectErrOtherIntervar(line)
            #print("apres detectErrOtherIntervar", l)
            if (retCode) : 
                (retCode, s) = replaceIntervarByValues(l, dIntervar, dJobObjectVersion, dDsx[dsjobIdentifier]['dsjobName'], dDsx[dsjobIdentifier]['dsjobVersion'])
                #print("apres replaceIntervarByValues", s)
                s = s.replace(" ", "")
                dDsx[dsjobIdentifier]['dsrecords'][dsrecordName]["rejets"][rejet] = s + TAB
            else :
                print(lineNumber, "Pb:", "+".join(l))
            if (bShowAll and bShowErrCode) :
                print(lineNumber, "ERR_Code :", line.strip(), TAB, " dsrecordName :", dsrecordName, " rejet :", rejet) 
            continue
            
        if (bMainloop and posErrDesc > 0 and posErrDesc < posEqual) : 
            bErrDesc = True
            errDescNumber += 1
            nbrMaxErrDescTmp += 1
            rejet = line[:posErrDesc - 1].strip()
            (retCode, l) = detectErrOtherIntervar(line)
            if (retCode) : 
                (retCode, s) = replaceIntervarByValues(l, dIntervar, dJobObjectVersion, dDsx[dsjobIdentifier]['dsjobName'], dDsx[dsjobIdentifier]['dsjobVersion'])
                dDsx[dsjobIdentifier]['dsrecords'][dsrecordName]["rejets"][rejet] += s
            else :
                print(lineNumber, "Pb:", "+".join(l))
            if (bShowAll and bShowErrDescription) :
                print(lineNumber, "ERR_Desc :", line.strip(), TAB, " dsrecordName :", dsrecordName, " rejet :", rejet) 
            continue
        
        if ((bInitialize or bMainloop) and posInterVar > -1 and posInterVar < posEqual) :
            intervarNumber += 1
            if (bMainloop and not bIf and bElse) :          
                intervarSsIfNumber += 1
                if (bShowAll and bShowIntervarElse) :
                    print(lineNumber, "Not if InterVar :", line.strip())
            else :
                ##  Intervar est, ou dans le bloc initialize, ou (dans le bloc mainloop ET dans un if (ou en dehors d'un bloc if !)
                # \"V\"
                # \"19000101\"
                # \"%yyyy%mm%dd\"
                # \"*\"
                # \"|\"
                # \"CIR\"
                # \"1\"
                # LN_Done.Row_Found_CIR2a
                # TRANSFORMER_psPrmJxWRK_pObjectCodeTo
                #  InterVar0_1 = InterVar0_0 / get_num_of_partitions();
                l = line.split("=", 1)
                ### Jamais detectee len(l) != 2 
                k = l[0].strip()
                v = l[1][:-1].strip() # suppression du ; final
                #v = v.replace('\\"', '') # suppression de \"
                v = v.lstrip('\\"').rstrip('\\"') # suppression des \" lateraux
                v = v.replace('\\', '') #suppression des \
                
                l = v.split("+")
                if (False and len(l) > 1) :
                    ## Les trucs pas standards ...
                    ## 781880	 ??? InterVar0_2 = (InterVar0_4 + InterVar0_5);
                    ## 781885	 ??? InterVar0_8 = julian_day_from_date(date_from_ustring(((InterVar0_0 + InterVar0_1) + InterVar0_2) + InterVar0_7)) - 1;
                    ## 
                    for item in l :
                        lTmp = re.findall('InterVar[0-9]+_[0-9]+', item,  re.IGNORECASE)
                        if (dDsx[dsjobIdentifier]['dsjobEnrichissement'] and len(lTmp) > 1) :
                            # print(lineNumber, "???", line)
                            # print(lineNumber, "???", lTmp)
                            # InterVar0_30 = trimc_string(LN_Done.NUCTSC , InterVar0_1 , InterVar0_10);
                            # InterVar0_26 = ((u_is_numeric(u_trimc_string(InterVar0_6 , InterVar0_22 , InterVar0_23)) == InterVar0_0) && (u_count_substring(InterVar0_7 , InterVar0_24) == 0)) && (u_count_substring(InterVar0_9 , InterVar0_25) == 0);
                            # InterVar0_7 = ((is_numeric(trimc_string(LN_Done.NCPTEI , InterVar0_3 , InterVar0_4)) == InterVar0_5) && (count_substring(LN_Done.NCPTEI , InterVar0_4) == 0)) && (count_substring(LN_Done.NCPTEI , InterVar0_6) == 0);
                            # InterVar0_2 = right_substring(trimc_string(string_from_decimal(LN_Done.QTEFFE , InterVar0_1) , InterVar0_8) , 5);
                            # InterVar0_6 = 4 - string_length(string_from_decimal((decimal_from_string(StageVar0_svAnnee) - InterVar0_4) , InterVar0_5));
                            # InterVar0_10 = julian_day_from_date(date_from_string((((StageVar0_svAnnee + InterVar0_7) + StageVar0_svMois) + InterVar0_8) , InterVar0_9)) - 1;
                            # julian_day_from_date(date_from_string((((StageVar0_svAnneeDDHISTO + InterVar0_1) + StageVar0_svMoisDDHISTO) + InterVar0_2) , InterVar0_3)) - 1;
                            ## 
                            ##  TODO
                            ##
                            pass
                        elif (len(lTmp) == 1) :
                            # print(lineNumber, ":-)", line)
                            # print(lineNumber, ":-)", lTmp)
                            ## 
                            ##  TODO
                            ##
                            pass
                        
                    
                
                if (True) :
                    if (v[0:8].upper() == "LN_DONE.") : 
                        v = v[8:]
                    ## Cas rare voir VAL_LIQUIDATIVE_PE_024_1
                    ## impose de faire mecanisme plus global
                    #if (v[-14:].upper() == "_POBJECTCODETO") : 
                    if (v.upper().find("POBJECTCODETO") > -1) :
                        if (dDsx[dsjobIdentifier]['dsjobEnrichissement'] == "VAL_LIQUIDATIVE_PE_024_1") :
                            #v = "VALW3097501"
                            v = "VAL" + dJobObjectVersion["VAL_LIQUIDATIVE_PE"] + "1"
                        else :
                            v = "<ObjectCodeTo>"
                    if (v[-19:].upper() == "NUM_OF_PARTITIONS()") :
                        v = v[:-26]
                    
                    ## Certaines affectation de interVar sont complexes
                    ##  Jx_S_DTA_WRK_Enrichissement_AFFECT_CENTR_INT_INTRL_025_1
                    ## InterVar0_8 = julian_day_from_date(date_from_ustring(((InterVar0_0 + InterVar0_1) + InterVar0_2) + InterVar0_7)) - 1;
                    # lComplexe = re.findall('InterVar[0-9]+_[0-9]+', v,  re.IGNORECASE)
                    # if (len(lComplexe) > 1) : 
                        # print("v :::", v)
                        # print("lComplexe", lComplexe)
                    
                    
                    #print("v[-14:] =", v[-14:], TAB, " intervar :", k, TAB, " =", v, TAB, " (", l[1], ")")
                    if (v[0:8].upper() == "INTERVAR") :
                        #print("INDIRECTE", line)
                        try :
                            v = dIntervar[v]
                        except :
                            pass
                        if (v[0:8].upper() == "INTERVAR") : ### Jamais detectee !
                            #print("INDIRECTE AGAIN !")
                            try :
                                v = dIntervar[v]
                            except :
                                pass
                # endif False
                
                
                
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

print("")
print("-------------------- dDsx --------------------")
#print(dDsx)
# for (k, v) in enumerate(dDsx) :
    # print(v, ":")
    # if (dDsx[v]['dsjobEnrichissement'] and dDsx[v]['dsjobPlanif']) :
        # for (i) in dDsx[v] :
            # print(TAB, i, "=", dDsx[v][i])

            
print("")
print("-------------------- Liste des jobs --------------------")
lCols = list()
#lCols.append("")
lCols.append("dsjobName")
lCols.append("dsjobVersion")
lCols.append("dsjobPlanif")
lCols.append("dsjobModifDate")
lCols.append("dsjobIdentifier")
#lCols.append("")
# for v in dDsx :
    # slOut = ""
    # for col in lCols :
        # slOut += str(dDsx[v][col]) + TAB
    # print(slOut)


print("")
print("-------------------- Out --------------------")
for dsjobId in dDsx : 
    if (dDsx[dsjobId]["dsjobName"]) : 
        sLineOut = dDsx[dsjobId]["dsjobName"] + TAB + dDsx[dsjobId]["dsjobVersion"] + TAB + dDsx[dsjobId]["dsjobModifDate"] + TAB 
        if (dDsx[dsjobId]['dsjobSource']) :
            sLineOut += dDsx[dsjobId]['dsjobSource'] + TAB 
        else :
            sLineOut += "Tbl src inconnue" + TAB + "Obj src ?" + TAB
        if (dDsx[dsjobId]["dsjobPlanif"]) :
            sLineOut += "au plan" + TAB 
        else :
            sLineOut += "inactif" + TAB 
        ##  
        for dsrecord in dDsx[dsjobId]["dsrecords"] : 
            for rejet in dDsx[dsjobId]["dsrecords"][dsrecord]["rejets"] :
                print(sLineOut + rejet + TAB + dDsx[dsjobId]["dsrecords"][dsrecord]["rejets"][rejet])



    
    
    