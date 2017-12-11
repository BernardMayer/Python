#!/python
# -*- coding: utf-8 -*-
### http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
from __future__ import unicode_literals
from __future__ import print_function

"""
Les modules pyodbc, pathlib, configparser ne sont pas disponibles 
sur nos machines Linux RedHat python 2.6.6
"""

# import cgitb
# cgitb.enable(format='text')

import sys
import os
#import string
#import pyodbc
#import pathlib
import argparse
#import configparser
import re
#from collections import OrderedDict
import collections
import time
import datetime
import decimal
#import xml
try :
    import xml.etree.cElementTree as ET
    print("usage de cElementTree", file=sys.stderr)
except :
    import xml.etree.ElementTree as ET
    print("usage de ElementTree", file=sys.stderr)

decimal.getcontext().prec = 2
TAB = '\t'
FileOutSep = TAB
FileOutHeader = False
Verbose = True
dtNow  = datetime.datetime.today()
tsNow = dtNow.timestamp()


def getRootinfos(s, dInfos) :
    '''
    '''
    retCode = False
    for info in dInfos :
        print("info=" + info, file=sys.stderr)
    return retCode, dInfos

## fichier a traiter
me = sys.argv[0]
#args = sys.argv[1:]
if (len(sys.argv) == 1) :
    print("Le fichier pjb dit etre le 1er parametre de " + me, file=sys.stderr)
    quit()
if (len(sys.argv) == 2) :
    pjbFilename = sys.argv[1]
    print("Traitement du fichier pjb " + pjbFilename, file=sys.stderr)
if (not os.path.exists(pjbFilename)) :
    print(pjbFilename + " est introuvable", file=sys.stderr)
    quit()

    
##  Faire l'inventaire des entities
##  https://stackoverflow.com/questions/14744945/parse-xml-with-xhtml-entities
##  Remplace &#x1D; par LF (http://www.asciitable.com/) Dec:10 Hex:A Oct:012

tree = ET.parse(pjbFilename)
#quit()
    
try :    
    tree = ET.parse(pjbFilename) # "D:/v2_DSX/dsx/" + 
except :
    print("Le fichier ", pjbFilename, "ne peut etre parse", file=sys.stderr)
    quit()
    
root = tree.getroot()
#print(root.get('lastModificationTimestamp'))


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
# dRootinfos['toto'] = root.get('toto')
# dRootinfos[''] = False
# dRootinfos[''] = False

## Trouver 
##  <contains_JobObject name=""
##      <of_DSMetaBag 
##          <has_DSMetaData name="" value=""
##          .ERR_Code etc etc etc
# //contains_JobObject/of_DSMetaBag/has_DSMetaData # sans le . devant, affiche un warning
for parent in tree.findall('.//contains_JobObject') :
    objName = parent.get("name")
    for node in parent.findall('./of_DSMetaBag/has_DSMetaData') : 
    #for node in tree.iter() : #.xpath('//DSJobDefSDO/of_DSMetaBag') :
        # print(root.get('name'))
        # print(node.tag, node.attrib) #.attrib
        subName = node.get('name')
        candidat = node.get('value')
        if (candidat.find(".ERR_") > -1) :
            print("---objName :", objName, TAB, "subName :", subName, file=sys.stderr)
            print(candidat, file=sys.stderr)
        pass

#print(dRootinfos)
quit()
