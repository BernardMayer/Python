#!/python
# -*- coding: utf-8 -*-
### http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
### https://pymotw.com/2/xml/etree/ElementTree/parse.html
from __future__ import unicode_literals
from __future__ import print_function

"""
Les modules pyodbc, pathlib, configparser ne sont pas disponibles 
sur nos machines Linux RedHat python 2.6.6
"""

import cgitb
cgitb.enable(format='text')

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
# try :
    # import xml.etree.cElementTree as ET
    # print("usage de cElementTree", file=sys.stderr)
# except :
    # import xml.etree.ElementTree as ET
    # print("usage de ElementTree", file=sys.stderr)

### https://pymotw.com/2/xml/etree/ElementTree/parse.html
from xml.etree.ElementTree import iterparse
depth = 0
prefix_width = 8
prefix_dots = '.' * prefix_width
line_template = '{prefix:<0.{prefix_len}}{event:<8}{suffix:<{suffix_len}} {node.tag:<12} {node_id}'




decimal.getcontext().prec = 2
TAB = '\t'
FileOutSep = TAB
FileOutHeader = False
Verbose = True
dtNow  = datetime.datetime.today()
tsNow = dtNow.timestamp()



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

# context = iterparse(pjbFilename, events=('start', 'end', 'start-ns', 'end-ns'))
# context = iter(context)
# event, root = context.next()
# for event, elem in context : 
    # pass

for (event, node) in iterparse(pjbFilename, events=('start', 'end')): # , 'start-ns', 'end-ns'
    if event == 'end':
        depth -= 1
        #print(event, TAB, node.tag)
        
        prefix_len = depth * 2
    #print(event, TAB, node.tag, id(node))
    #print line_template.format(prefix=prefix_dots, prefix_len=prefix_len, suffix='', suffix_len=(prefix_width - prefix_len), node=node, node_id=id(node), event=event)
    
    if event == 'start':
        depth += 1
        if (node.tag == "{http:///com/ibm/datastage/ai/dtm/ds.ecore}DSJobDefSDO") :
            # name
            print("name =", node.attrib.get('name'), end = "")
            # lastModificationTimestamp
            print(", lastModificationTimestamp", node.attrib.get('lastModificationTimestamp'))
            # modifiedByUser
            print(", modifiedByUser =", node.attrib.get('modifiedByUser'), end = "")
            # creationTimestamp
            print(", creationTimestamp =", node.attrib.get('creationTimestamp'), end = "")
            # jobType
            print(", jobType =", node.attrib.get('jobType'), end = "")
            # version
            print(", version =", node.attrib.get('version'), end = "")
            # shortDescription
            print(", shortDescription =", node.attrib.get('shortDescription'), end = "")
            # category
            print(", category =", node.attrib.get('category'), end = "")
            # dSNameSpace
            print(", dSNameSpace =", node.attrib.get('dSNameSpace'), end = "")
            # dSJobType
            print(", dSJobType =", node.attrib.get('dSJobType'))
        ##  has_DSMetaData 
        if (node.tag == "has_DSMetaData") :
            val = node.attrib.get('value')
            if (val.find("initialize {") > -1) :
                # name
                print("name =", node.attrib.get('name'), end = "")
                # value
                print(", value =", node.attrib.get('value')[0:333])