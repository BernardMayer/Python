#!/python
# -*- coding: utf-8 -*-


"""
gps2db <db> <fichier.gpx>

connecter à la db
ouvrir le fichier GPX
pour chaque element 
    le stocker dans la DB
fermer la db
fermer le fichier
rendre compte
"""


# Diff Python2 vs python3
# https://python.doctor/page-syntaxe-differente-python2-python3-python-differences

# Pour que les print() fonctionnent
# en python2 (serveurs datastage) ET en python3 (poste de travail)
# print "\n".join([x, y])         -->   print(x, y, sep="\n")
# print >> sys.stderr, "erreur"   -->   print("Erreur", file=sys.stderr)
# print "une ligne ",             -->   print("une ligne", end="")
from __future__ import print_function
