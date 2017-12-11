#!/python
# -*- coding: utf-8 -*-
### http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
from __future__ import unicode_literals

"""
Les modules pyodbc, pathlib, configparser ne sont pas disponibles 
sur nos machines Linux RedHat python 2.6.6
"""
#####
import pdb
#####
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
        logErr("Le fichier dictionnaire [" + f + "] ne peut etre ouvert !")
        logErr("except ({0}) : {1}".format(e.errno, e.strerror))
        quit()
    except :
        logErr("Le fichier dictionnaire [" + f + "] ne peut etre ouvert !")
        logErr("erreur : " + str(sys.exc_info()[0]))
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

def forgeErrorString(s, d, dJov) :
    ''' Traitement des lignes qui elaborent les codes et description d'erreurs
    ERR_Code et ERR_Description
    s est la ligne brute, d est le dictionnaire contenant les variables
    s = [  LN_Reject_1.ERR_Code = ((InterVar0_12 + InterVar0_13) + InterVar0_14);]
    ! Quelques configurations plus complexes ; par exmple dans 
    extrait de s = [...  + InterVar0_26) + u_trimc_string(InterVar0_21 , InterVar0_25)) + InterVar0_27 ...]
    '''
    # Suppression du ";" final, et
    # ret = de la position du caractere "=" + une position jusqu'a la fin
    # ret = [ ((InterVar0_12 + InterVar0_13) + InterVar0_14)]
    ret = s[s.find("=") + 1:].replace(";", "")
    # Suppression des espaces et des parentheses
    # ret = [InterVar0_12+InterVar0_13+InterVar0_14]
    ret = ret.replace("(", "").replace(")", "").replace(" ", "")
    # Ventilation de cette string vers une liste (tableau)
    l = re.findall("InterVar[0-9]*_[0-9]*", s)
    # Affectation / remplacement des elements du tableau (clefs) par leurs valeurs associees
    # l[0] = "InterVar0_12" --> l[0] = "LN_Done.CD_EDS_BNQ;"
    ret = ""

    for k in d :
        v = d[k]
        # 
        # Pour resoudre   InterVar0_15 = InterVar0_16
        #
        #if (d.has_key(v)) :   # obsolete en Python 3
        if (v in d) :
            d[k] = d[v]
            #
            #print("Remplacement par :", d[k])  
        #
        #print("key =", k, "val=[" + v + "]") 
        
        #
        # Pour resoudre   InterVar0_10 = (((((InterVar0_52 + InterVar0_25) + InterVar0_53) + InterVar0_27) + InterVar0_28) + InterVar0_29) + InterVar0_54;
        # voir Jx_S_DTA_WRK_Enrichissement_ACTN_CRED_COMPLEXE_026_1
        #
        lTmp = re.findall("InterVar[0-9]*_[0-9]*", v)
        if (len(lTmp) > 1) : 
            vTmp = v.replace("(", "").replace(")", "").replace(" ", "")
            lTmp = re.findall("InterVar[0-9]*_[0-9]*", v)
            retTmp = ""
            for i in lTmp :
                retTmp += d[i] + " " 
            d[k] = retTmp
        
        #
        # Pour resoudre le code objet (ObjectCodeTo)
        # \(9)\(9)InterVar0_20 = TRANSFORMER_psPrmJxWRK_pObjectCodeTo;
        #


    for i in l : 
        #
        #print("i = ", i)
        # print("i = ", i, "v =", d[i])
        ret += d[i] + " "
    
        
    #
    #print("s =", s)
    return ret                
                    

def parseDsx(d, dJov, dVer) : 
    '''
    '''
    ret = False
    nLine = 0
    bDebut = True
    bHeader = bDsjob = bDsjobHeader = bInitialize = bMainloop = bFinish = False
    headerServerName = headerToolInstanceID = headerDate = ""
    #dsjobDateModified = dsjobTimeModified = ""
    #dsjobIdentifier = dsjobIdentifierClean = ""
    sErr = ""
    bIf = bElse = False
    with open(d['path'] + os.sep + d['name']) as fDsx : #, encoding='utf_8'
        #
        #print("fDsx =", d['path'] + os.sep + d['name'])
        for line in fDsx.readlines() :
            nLine += 1
            if (bDebut and line[0:12] == 'BEGIN HEADER') :
                bDebut = False
                bHeader = True
            #if (bHeader and line[0:11] == 'BEGIN DSJOB') : # bHeader and ne fonctionne que s'il y a un seul job dans le fichier
            if (line[0:11] == 'BEGIN DSJOB') :
                bHeader = False
                bDsjob = True
                bDsjobHeader = True
                dsjobIdentifier = dsjobIdentifierClean = ""
                dsjobDateModified = dsjobTimeModified = ""
                dsjobNameVersion = dsjobName = dsjobVersion = ""
            if (bDsjob and line[0:12] == 'initialize {') :
                bDsjobHeader = False
                bInitialize = True
                ## Creation du dictionnaire des variables InterVar
                dIntervar = dict()
            if (bInitialize and line[0:10] == 'mainloop {') :
                bInitialize = False
                bMainloop = True
                #
                #print("dIntervar :", dIntervar, "ligne = ", nLine)
            if (bMainloop and line[0:8] == 'finish {') :
                bMainloop = False
                bFinish = True
            if (bMainloop and line.find(' if (')) :
                bIf = True
            if (bMainloop and bIf and line == " }") :
                bIf = False
            if (bFinish and line[0:9] == 'END DSJOB') :
                ## Derniere ligne du fichier ...
                bDsjob = False
              

            
            if (bMainloop) :
                bErrCode = bErrDesc = False
                sErrCode = sErrDesc = ""
                line = line.replace('\r', "").replace('\n', "")
                line = line.replace('\\(9)', "").replace('\t', "")
                # if (bIf and line[0:10] == '  InterVar') :
                #if (line[0:10] == '  InterVar') :
                #if (re.match("InterVar[0-9]*_[0-9]*\b=\b", line)) :
                if (bIf and line.lstrip()[:8] == "InterVar" and line.find(" = ") > 0) :
                    bElse = False
                    #
                    #print("bIf et intervar", line)
                    #
                    #print(TAB, "[" + line.lstrip()[:8] + "]")
                    #print("re.match", re.match("InterVar[0-9]*_[0-9]*", line)) InterVar[0-9]*_[0-9]*
                    #print("len(lIntervar) =", len(lIntervar))
                    #line = line.replace('\r', "").replace('\n', "")
                    line = line.rstrip(";")
                    lIntervar = line.split('=')
                    if (len(lIntervar) > 1) : 
                        k = lIntervar[0].replace(" ", "")
                        lIntervar.pop(0)
                        dIntervar[k] = "=".join(lIntervar).replace(" ", "")
                        #
                        #print("k =", k, " ? ", dIntervar[k])
                        ## Transformer   LN_Done.CD_EDS_BNQ   en   <CD_EDS_BNQ>
                        l = dIntervar[k].split(".")
                        if (len(l) == 2) : 
                            #
                            #print("DOT", dIntervar[k])
                            dIntervar[k] = "<" + l[1] + ">"
                        
                        ##
                        ##
                        ## dsjobIdentifier == Jx_Sn_DTA_WRK_Enrichissement_EMAIL_024_1
                        ##
                        if (dIntervar[k][-14:] == "_pObjectCodeTo") : 
                            #logWarn("BINGO ! " + dIntervar[k])
                            #logWarn("dsjob = " + dsjobIdentifier + " alias_name = " + dsjobIdentifier[29:])
                            #if dJov.has_key(dsjobIdentifier) : # obsolete en Python 3
                            if (dsjobIdentifier in dJov) :
                                #dIntervar[k] = dJov[dsjobIdentifier[29:]]
                                #logWarn("BINGO ! " + dIntervar[k])
                                pass

                        ## Transformer   TRANSFORMER_psPrmJxWRK_pObjectCodeTo   en   <ObjectCodeTo>
                        l = dIntervar[k].split("_")
                        if (len(l) == 3) :
                            ## Suppression de la lettre p si elle existe
                            if (l[2][:1] == 'p') :
                                l[2] = l[2][1:]
                            dIntervar[k] = "<" + l[2] + ">"
                    if (line.find(" else ")) :
                        bIf = False
                
                if (line.upper().find("ERR_CODE") > 0) :
                    bErrCode = True
                    # sErrCode = line[line.find("=") + 1:].replace(";", "")
                    # sErrCode = sErrCode.replace("(", "").replace(")", "")
                    # try : 
                    sErrCode = forgeErrorString(line, dIntervar, dJov)
                    ## Verifier conformite sErrCode
                    ## remplacer <ObjectCodeTo> par sa valeur
                    ## CIR <ObjectCodeTo> 9   -->   CIRW01234Z9
                    sErrCode = sErrCode.strip()
                    errType = sErrCode[0:3].replace('"', '').strip()
                    errObjcodeto = sErrCode[4:19]
                    errNum = sErrCode[19:].replace('"', '').strip()
                    #try :
                        
                    
                    k = dsjobName + "_" + dsjobVersion
                    if (k in dJov) :
                        errObjcodeto = dJov[k]
                        #sErr = "[" + sErrCode + "]-->" + errType + "*" + dJov[k] + "*" + errNum
                        sErr = errType + errObjcodeto + errNum
                    else : 
                        k = dsjobName
                        if (k in dJov) :
                            errObjcodeto = dJov[k]
                            #sErr = sErrCode + " (" + dJov[k] + ")"
                            sErr = "?" + errType + errObjcodeto + errNum + "?"
                            errObjcodeto = "?" + errObjcodeto + "?"
                            sJobValid = ""
                        else :
                            sErr = sErrCode

                            
                
                if (line.upper().find("ERR_DESCRIPTION") > 0) :
                    bErrDesc = True
                    # try : 
                    sErrDesc = forgeErrorString(line, dIntervar, dJov)
                    sErr += TAB + sErrDesc

                    ## Sauvegarder les informations !
                    if (True) :
                        print( \
                            TAB + \
                            sJobValid + TAB + \
                            headerServerName + TAB + \
                            headerToolInstanceID + TAB + \
                            headerDate + TAB + \
                            dsjobIdentifier + TAB + \
                            dsjobDateModified + TAB + \
                            dsjobTimeModified + TAB + \
                            sErr + TAB + \
                            ####dsjobNameVersion + TAB + \
                            dsjobName + TAB + \
                            dsjobVersion + TAB + \
                            errType + TAB + \
                            errObjcodeto + TAB + \
                            errNum
                            )  
                    
                
            if (bInitialize) :
                #InterVar0_4 = 1;
                #InterVar0_31 = \"ALI:=\";
                line = line.replace('\r', "").replace('\n', "")
                line = line.replace('\\(9)', " ").replace('\t', " ")
                if (line[0:9] == ' InterVar') :
                    
                    lIntervar = line.split('=')
                    if (len(lIntervar) > 1) : 
                        k = lIntervar[0].replace(" ", "")
                        lIntervar.pop(0)
                        v = "=".join(lIntervar)
                        v = v[:-1] # suppr dernier char (;)
                        v = v.replace('\\"\'', '') # \"'
                        v = v.replace('\'\\"', '') # '\"
                        v = v.replace('\\"', '') # \"
                        v = v.replace('\\', '') # \
                        v = v.replace('\t', '') # \t
                        v = v.lstrip() # == trim()
                        v = v.rstrip() # == trim()
                        dIntervar[k] = v
                        #
                        #print (k, TAB, v)
            
            if (bDsjob and bDsjobHeader) :
                line = line.replace('\r', "").replace('\n', "").replace('\\(9)', " ")
                if (line[0:17] == '   TimeModified "') : 
                    dsjobTimeModified = line[17:-1]
                if (line[0:17] == '   DateModified "') : 
                    dsjobDateModified = line[17:-1]
                if (line[0:15] == '   Identifier "') : 
                    dsjobIdentifier = line[15:-1]
                    sJobValid = ""
                    print("IDENTIFIER !", line)
                    #print(line, end=TAB)
                    
                    ## Supprimer la partie versionning
                    ## Jx_S_DTA_WRK_Enrichissement_ADI_A_024_1 --> Jx_S_DTA_WRK_Enrichissement_ADI_A
                    ##dsjobIdentifierClean = re.sub('_[a-zA-Z]{0,}[0-9]{1,}_[0-9]{1,}$', "", dsjobIdentifier)
                    # lVersion == <job> <version majeure> <version mineure> == Jx_S_xxxxx_E27_2
                    # Supprimer le prefixe, Thomas dit toujours 5 partie separees par _
                    # Jx_S_DTA_WRK_Enrichissement_ADI_A_024_1 --> ADI_A_024_1
                    lTmp = dsjobIdentifier.split('_', 5)
                    try :
                        #print("lTmp[0]", lTmp[0], "lTmp[4]", lTmp[4])
                        if (lTmp[0][0:1].upper() == "J" and lTmp[4].upper() == "ENRICHISSEMENT") :
                            dsjobNameVersion = lTmp[5]
                            #print("dsjobNameVersion", dsjobNameVersion)
                            sJobValid = "Valid"
                    except :
                        #print("EXCEPT dsjobIdentifier", dsjobIdentifier, "LINE", line)
                        pass

                    ## Tester la validite de la version
                    ## Si la version est correcte, alors le nom est correct
                    if (sJobValid) :
                        lTmp = dsjobNameVersion.rsplit('_', 2)
                        #print("lTmp[0]", lTmp[0], "lTmp[1]", lTmp[1], "lTmp[2]", lTmp[2])
                        if (lTmp[2].isdigit()) :
                            #print("int(lTmp[2])", int(lTmp[2]))
                            if (int(lTmp[2]) > 100 and int(lTmp[2]) < 10000) :
                                dsjobVersion = lTmp[2]
                                #print("dsjobVersion INT =", dsjobVersion)
                                # Jx_S_DTA_WRK_Enrichissement_A_BDF_MENS_1002
                                # lTmp[0]==A_BDF lTmp[1]==MENS lTmp[2]==1002
                                dsjobName = lTmp[0] + "_" + lTmp[1]
                            else :
                                if (lTmp[1].isdigit() and int(lTmp[1]) < 100) : 
                                    dsjobVersion = lTmp[1] + "_" + lTmp[2]
                                    #print("dsjobVersion INT_INT =", dsjobVersion)
                                else :
                                    if (lTmp[1][0:1].isalpha() and lTmp[1][1:].isdigit() and int(lTmp[1][1:]) < 100) :
                                        dsjobVersion = lTmp[1] + "_" + lTmp[2]
                                        #print("dsjobVersion XINT_INT =", dsjobVersion)
                                    else :
                                        sJobValid = ""
                                        #print("???")
                                if (sJobValid) : 
                                    dsjobName = lTmp[0]
                        ## Controle que la version existe bien, sinon, pas valide !
                        if (not dsjobVersion in dVer) : 
                            sJobValid = ""
                            

                        
                    # try :
                        # lVersion = dsjobIdentifier.rsplit('_', 2) 
                        # dsjobVersion = lVersion[1] + "_" + lVersion[2]
                    # except :
                        # dsjobVersion = ""
                    
                    #
                    #print("dsjobIdentifier =", dsjobIdentifier, TAB, len(dsjobIdentifier.split('_')), os.linesep)
                    
                #if (dsjobIdentifier and dsjobDateModified and dsjobTimeModified) :
                    #bDsjobHeader = False
            
            if (bHeader) :
                # Bloc BEGIN HEADER
                line = line.replace('\r', "").replace('\n', "")
                if (line[0:8] == '   Date ') : 
                    headerDate = line[9:-1]
                if (line[0:18] == '   ToolInstanceID ') : 
                    headerToolInstanceID = line[19:-1]
                if (line[0:14] == '   ServerName ') : 
                    headerServerName = line[15:-1]
    #
    #print("headerServerName =", headerServerName, "headerToolInstanceID =", headerToolInstanceID, "headerDate =", headerDate)
    #print("dsjobIdentifier =", dsjobIdentifier, "dsjobDateModified =", dsjobDateModified, "dsjobTimeModified =", dsjobTimeModified)
    
    return ret


def callParser(d, dJov, dVer) :
    ''' Parcourt la liste de fichier
    et appelle le parser SI ([<key>]['useit'] est True
    ''' 
    i = ok = 0
    for k in d :
        #
        #print("k =", k)
        #print("type d[k]:", type(d[k]))
        if (d[k]['useit']) :
            i += 1
            # 
            #print("callParser() pour", k)
            #print("- - - - - - -")
            ret = parseDsx(d[k], dJov, dVer)
            if (ret) :
                ok += 1
        else :
            #
            #print(k, "abandon")
            pass
    return ok


def logListTodoDsxfiles(d) :
    ''' A partir de d (liste des fichiers DSX,
    genere une string des fichiers a traiter / parser
    '''
    ret = os.linesep + "Liste des fichiers a traiter / parser : " + os.linesep
    for k in d :
        if (d[k]['exist'] and d[k]['useit']) :
            ret += TAB + d[k]['name'] + os.linesep
    return ret + os.linesep
    

def setListeValues(d, lastrun) :
    ''' pour chaque item du dict :
            a partir de path et name, verifier existence
            recuperer la valeur de mtime, la placer dans le dict
            etablir d'apres lastrun si useit passe a True
    '''
    for k in d :
        #
        #print("k =", k)
        #print("type d[k]:", type(d[k]))
        fileFullName = d[k]['path'] + os.sep + d[k]['name']
        if (os.path.exists(fileFullName)) :
            d[k]['mtime'] = int(os.path.getmtime(fileFullName))
            if (d[k]['mtime'] > lastrun) :
                d[k]['useit'] = True
        else : 
            logWarn("Fichier DSX " + fileFullName + " introuvable")
            d[k]['useit'] = False
    return d

    
def getFileList() :
    ''' Lire le fichier et le mettre dans une structure de donnees
    '''
    fileFullName = dIni['listFile']
    # Existe t-il ?
    if (os.path.exists(fileFullName)) :
        dFiles = dict()
        with open(fileFullName, 'r') as fDsxList :
            for line in fDsxList.readlines() :
                line = line.replace('\r', "").replace('\n', "")
                if (len(line) == 0 or (not line[0].isalnum() and line[0] != "$")) :
                    continue
                dFiles[line] = dict()
                dFiles[line]['path']  = dIni['dsxHome']
                dFiles[line]['name']  = line
                dFiles[line]['exist'] = True
                dFiles[line]['mtime'] = 0
                dFiles[line]['useit'] = False
        fDsxList.close()    
        return dFiles
    else :
        logErr("Fichier liste desDSX [" + fileFullName + "] est introuvable !")
        quit()


def getLastrun() :
    ''' Recupere le TS de la derniere execution, 
    0 par defaut
    '''
    mtimeVar = 0
    mtimeBin = 0
    # nom fichier sans extension
    (pgmNamePath, pgmName) = os.path.split(sys.argv[0])
    (pgmNameShort, pgmNameExt) = os.path.splitext(pgmName)
    # Un fichier lastrun existe t-il dans le repertoire etc ?
    lastrunFilename = pgmNameShort + ".lastrun.txt"
    lastrunFullFilename = pgmNamePath + os.sep + ".." + os.sep + "var" + os.sep + lastrunFilename
    if (os.path.exists(lastrunFullFilename)) : 
        mtimeVar = os.path.getmtime(lastrunFullFilename)
        # Le contenu du fichier est-il valide ?
        with open(lastrunFullFilename, 'r') as fLastrun : 
            ligne = fLastrun.readline()
            ligne = ligne.replace('\r', "").replace('\n', "")
            fLastrun.close()
        ts = str2ts(ligne)
        if (ts) : 
            return ts
    else :
        lastrunFullFilename = pgmNamePath + os.sep + lastrunFilename
        if (os.path.exists(lastrunFullFilename)) : 
            mtimeBin = os.path.getmtime(lastrunFullFilename)
            with open(lastrunFullFilename, 'r') as fLastrun : 
                ligne = fLastrun.readline()
                ligne = ligne.replace('\r', "").replace('\n', "")
                fLastrun.close()
            ts = str2ts(ligne)
            if (ts) : 
                return ts
    
    return max(mtimeVar, mtimeBin)

    
def str2ts(s) :
    ''' Transforme une chaine
        en Epoch, sans en connaitre le format
        * ts
        * SSAAMMJJhhmiss
        * SSAA-MM-JJ[ hh:mi:ss]
        * JJ/MM/SSAA[ hh:mi:ss]
    '''
    ret = False
    # Si c'est un nombre, c'est OU un TS, ou une date ISO sans espace
    #
    #print("s=[", s, "]")
    for i in s :
        if (not i.isdigit() and not i in ("/", "-")):
            return False
    ccyy = mo = dd = hh = mi = ss = 0
    if (len(s) == 19) : 
        # dd/mo/ccss hh:mi:ss   or   ccss-mo-dd hh:mi:ss
        hh = int(s[11:13])
        mi = int(s[14:16])
        ss = int(s[17:])
        s = s[0:10]
    if (len(s) == 10 and not s.isdigit()) : 
        # dd/mo/ccss   or   ccss-mo-dd
        if (s[2] == "/" and s[5] == "/") :
            ccyy = int(s[6:])
            mo   = int(s[3:5])
            dd   = int(s[0:2])
        if (s[4] == "-" and s[7] == "-") :
            ccyy = int(s[0:4] )
            mo = int(s[5:7] )
            dd = int(s[8:])
    # ccyymoddhhmiss    
    if (len(s) == 14 and s.isdigit()) :
            hh = int(s[8:10])
            mi = int(s[10:12])
            ss = int(s[12:])
            s  = s[0:8]
    if (len(s) == 8 and s.isdigit()) :
        # ccyymodd
        if (int(s) < 19991231 and int(s) > 22861120) :
            return False
        else :    
            ccyy = int(s[0:4])
            mo = int(s[4:6])
            dd = int(s[6:])

    # Est-ce un TS raisonnable ?
    if (len(s) == 10 and s.isdigit()) :
        if (int(s) > 915145200 and int(s) < 2000000000) : 
            return int(s)
        else :
            return False
            
    try :
        dt = datetime.datetime(ccyy, mo, dd, hh, mi, ss)
        ret = int(dt.timestamp())
    except :
        ret = False
    
    return ret
    

def lireConfig() :
    ''' Lire la ligne de commande, y trouver le nom du fichier de configuration
    S'il n'est pas fourni, ce sera le nom du script, suffixé par .ini ou .cfg
    '''
    ##  Lire la ligne de commande pour recuperer le fichier ini
    # set dIni['cmdLine'], dIni['iniFile']
    
    getCmdline()
    
    ##  Lire de fichier de configuration ...
    # set dIni["objCfg"]
    # desactive en prevision Linux RH + Python 2.6.6
    # getInifile()
    # ! 
    
    return dIni

    
def getInifile() : 
    ''' Recuperer le fichier de configuration,
    le stocker dans la structure dIni
    '''
    global Verbose
    cfg = configparser.ConfigParser()
    cfg.read(dIni['iniFile'])  
    dIni["objCfg"] = cfg
    ##   Niveau de verbose
    if (cfg.has_option('GENERAL', 'verbose') and len(cfg['GENERAL']['verbose'].strip()) > 0) :
        Verbose = dIni['verbose'] = myStr2bool(cfg['GENERAL']['verbose'].strip())


def getCmdline() :
    ''' Analyser la ligne de commande
    On attend --ini ou --cfg avec le nom du fichier de configuration,
    sinon, le nom du script, suffixé par .ini ou .cfg
    '''
    cfgFileExtRequired = ('.ini', '.cfg')
    (cfgFilePath, cfgFileName) = os.path.split(sys.argv[0])
    (cfgFileNameShort, cfgFileNameExt) = os.path.splitext(cfgFileName)
    
    dIni['cmdLine'] = " ".join(sys.argv)
    parser = argparse.ArgumentParser()
    #parser.add_argument("-c", "--cfg",          required = True, dest='cfgFile',        help="Le fichier de configuration est obligatoire") # , default=cfgFileFullName
    parser.add_argument("-c", "--cfg",  dest='cfgFile',  default=None, help="Le nom du fichier de configuration.cfg")
    parser.add_argument("-i", "--ini",  dest='iniFile',  default=None, help="Le nom du fichier de configuration.ini")
    parser.add_argument("-l", "--list",    required = True, dest='listFile', default=None, help="Le nom du fichier liste_des_dsx.lst")
    parser.add_argument("-d", "--dsxHome", required = True, dest='dsxHome', default=None, help="Emplacement du fichier liste_des_dsx.lst")
    parser.add_argument("-j", "--jobObjectVersion", required = True, dest='fJobObjectVersion', default=None, help="Emplacement du fichier job object version")
    args = parser.parse_args()
    
    dIni['listFile'] = args.listFile
    dIni['dsxHome']  = args.dsxHome
    dIni['fJobObjectVersion']  = args.fJobObjectVersion
    
    # La version de travail, sous RedHet + Python2.6.6 
    # ne connait pas le module qui permet d'utiliser les fichiers .INI (configparser)
    # donc --> return pour desactiver la partie iniFile / cfgFile
    return
    
    if (not args.cfgFile and not args.iniFile) :
        #not os.path.exists(args.cfgFile) and not os.path.exists(args.iniFile)): 
        logErr("Fichier configuration ini ou cfg non fourni")
        for ext in cfgFileExtRequired :
            cfgFileFullName = os.path.join(cfgFilePath, cfgFileNameShort) + ext
            if (os.path.exists(cfgFileFullName)) :
                dIni['iniFile'] = cfgFileFullName
                break
        if (not 'iniFile' in dIni) :
            logErr("Configuration : Fichier de configuration PAR DEFAUT [" + cfgFileNameShort+ "] (.ini ou .cfg) introuvable")
            exit(2)
    else :
        if (args.iniFile) :
            dIni['iniFile'] = args.iniFile
        else : 
            dIni['iniFile'] = args.cfgFile
        # Test de la presence du fichier ini
        if (not os.path.exists(dIni['iniFile'])) :
            logErr("Configuration : Fichier de configuration FOURNI [" + cfgFileNameShort+ "] (.ini ou .cfg) introuvable")
            exit(1)
    return

    
def alert(p) :
    ''' Je ne sers pas a grand chose
    '''
    showinfo("Alerte", p)

    
def log(s) :
    ''' Ecrire INFO : sur la sortie standard
    '''
    print("INFO :", str(s), file=sys.stdout)
    return True

    
def logWarn(s) :
    ''' Ecrire WARNING : sur la sortie standard
    '''
    print("WARNING :", str(s), file=sys.stderr)
    return True

    
def logErr(s) :
    ''' Ecrire sur la sortie des erreurs
    '''
    print("ERROR :", str(s), file=sys.stderr)
    return True

    
def pointeuse() :
    ''' Retourne un horodatage
    '''
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
def myStr2bool(v) :
    ''' Retourne True ou False suivant une valeur de type String
    '''
    return v.lower() in ("yes", "true", "y", "t", "1", "oui", "o")


def myIsNumber(s) : 
    ''' Retourne True ou False si la valeur est un nombre (nn.nnn)
    '''
    try :
        float(s)
        return True
    except ValueError :
        return False

    
if __name__ == '__main__':
    print("Je suis le module principal d'une application, pas une application")
