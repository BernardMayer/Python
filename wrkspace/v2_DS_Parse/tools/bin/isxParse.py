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

def getLinkId(d, id, s) :
    #print("recherche du parent de " + id)
    if (not d.get(id, False)) :
        return "Id inconnu"
    valeurs = list(d[id].values())
    if (valeurs) :
        valeur = valeurs[0]
        #print("valeur =", valeur, "clefs =", d[id].keys())
        if (valeur == s) :
            # print("bingo")
            return id #list(d[id].keys())
        else :
            # print("recur")
            for k in list(d[id].keys()) :
                # print("for recur")
                return getLinkId(d, k, s)
    else :
        return "?"
        
## fichier a traiter
me = sys.argv[0]
#args = sys.argv[1:]
if (len(sys.argv) == 1) :
    print("Le fichier isx dit etre le 1er parametre de [" + me + "]", file=sys.stderr)
    quit()
if (len(sys.argv) == 2) :
    isxFilenameFull = sys.argv[1]
    if (os.path.isfile(isxFilenameFull) and os.access(isxFilenameFull, os.R_OK)) : 
        print("Traitement du fichier isx [" + isxFilenameFull + "]", file=sys.stderr)
    else :
        print("! Le fichier isx [" + isxFilenameFull + "] est introuvable / inacessible", file=sys.stderr)
        exit()

# try:
    # with open(isxFilenameFull) as isxFile :
        # pass
        # print("ouvert !")
# except IOError as e:
    # print("! Ouverture de [" + isxFilenameFull + "] impossible") #Does not exist OR no read permissions
    # exit()

##  Faire l'inventaire des entities
##  https://stackoverflow.com/questions/14744945/parse-xml-with-xhtml-entities
##  Remplace &#x1D; par LF (http://www.asciitable.com/) Dec:10 Hex:A Oct:012

# une liste de dict
# chaque dict contient les infos sur un stage
lStages = list()
dIds = dict()
dIsSrc = dict()
dHasSrc = dict()
dSrc = dict()
lIsSrc = list()
lHasSrc = list()
lSrc = list()
lTgt = list()

try :    
    # ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    # ET.register_namespace('xmi', "http://www.w3.org/1999/xhtml")
    tree = ET.parse(isxFilenameFull) # "D:/v2_DSX/dsx/" + 
except Exception as e:
    print("Le fichier [", isxFilenameFull, "] ne peut etre parse", file=sys.stderr)
    print(e, file=sys.stderr)
    quit()

root = tree.getroot()
dRootinfos = dict()
dRootinfos['lastModificationTimestamp'] = root.get('lastModificationTimestamp')
dRootinfos['creationTimestamp'] = root.get('creationTimestamp')
dRootinfos['modifiedByUser'] = root.get('modifiedByUser')
dRootinfos['name'] = root.get('name')
dRootinfos['shortDescription'] = root.get('shortDescription')
dRootinfos['jobType'] = root.get('jobType')
dRootinfos['version'] = root.get('version')
dRootinfos['category'] = root.get('category')
dRootinfos['dSNameSpace'] = root.get('dSNameSpace')
dRootinfos['dSJobType'] = root.get('dSJobType')
#print(dRootinfos)

#jobName = os.path.basename(isxFilenameFull)
for parent in tree.findall('.//contains_JobObject') :
    objName = parent.get("name")
    #print("Parent=" + objName)
    parentId = parent.get('{http://www.omg.org/XMI}id')
    #for node in tree.iter() : #.xpath('//DSJobDefSDO/of_DSMetaBag') :
    # for node in parent.findall('./of_DSMetaBag/has_DSMetaData') : 
    for node in parent.findall('./contains_FlowVariable') : 
        dNode = dict()
        dNode['job'] = dRootinfos['name']
        dNode['stage'] = parent.get("name")
        dNode['id'] = node.get('{http://www.omg.org/XMI}id')
        dNode['name'] = node.get('name', "")
        dNode['isSrc'] = node.get('isSourceOf_FlowVariable', "").strip()
        dNode['hasSrc'] = node.get('hasSource_FlowVariable', "").strip()
        dNode['srcColId'] = node.get('sourceColumnID', "")
        dNode['colRef'] = node.get('columnReference', "")
        dNode['tblDef'] = node.get('tableDef', "")
        dIds[dNode['id']] = dNode
        # print(dNode)
        if (False) :
            print(node.tag, node.attrib)
        ##Fabrication des listes des IDs des sources et des IDs des cibles
        indic = ""
        if (dNode['tblDef'] != "" and dNode['colRef'] != "") :
            # Ce node est ou une source ou une target
            # indic = dNode['colRef']
            if (dNode['isSrc'] != "") :
                # Ce node est une source
                indic = "SRC"
                lSrc.append(dNode['id'])
            else :
                # Ce node est une cible
                indic = "TGT"
                lTgt.append(dNode['id'])
        
        # print(dNode['job'] + TAB + dNode['stage'] + TAB + dNode['name'] + TAB + dNode['id'] + TAB + "isSrc=" + dNode['isSrc'] + TAB + "hasSrc=" + dNode['hasSrc'] + TAB + "srcColId=" + dNode['srcColId'] + TAB + "colRef=" + dNode['colRef'] + TAB + "tblDef=" + dNode['tblDef'])
        
        ## Fabrication du dict des IDs source
        if (dNode['isSrc'] != "") :
            liste = dNode['isSrc'].split(" ")
            for idSrc in liste :
                d = dict()
                d[idSrc] = "SRC"
                if (dNode['id'] in dIsSrc) :
                    dIsSrc[dNode['id']].update(d)
                else :
                    dIsSrc[dNode['id']] = d
                if (dNode['id'] in dSrc) :
                    dSrc[dNode['id']].update(d)
                else :
                    dSrc[dNode['id']] = d
        ## Fabrication du dict des IDs cible
        if (dNode['hasSrc'] != "") :
            liste = dNode['hasSrc'].split(" ")
            for idHas in liste :
                d = dict()
                d[idHas] = "TGT"
                if (dNode['id'] in dHasSrc) :
                    dHasSrc[dNode['id']].update(d)
                else :
                    dHasSrc[dNode['id']] = d
                if (dNode['id'] in dSrc) :
                    dSrc[dNode['id']].update(d)
                else :
                    dSrc[dNode['id']] = d
                
# print(dIds)        
# print("dIsSrc\n", dIsSrc)
# print("dHasSrc\n", dHasSrc)
# print("dSrc\n", dSrc)

for id in lTgt :
    #print(id, "\t:\t", getLinkId(dSrc, id, "SRC"))
    print("\nPour l'info en sortie : " + id + "\t" + dIds[id]['colRef'])
    #    print("entree via : " + " ".join(getLinkId(dSrc, id, "SRC")))
    print("entree via : ", getLinkId(dSrc, id, "SRC"))
    #print("\t entree = ", " ".join(getLinkId(dSrc, id, "SRC")) )
