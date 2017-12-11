"""
Explore une liste de fichiers jobs datastage au format dsx
pour extraire :
 - Les chaines de caracteres de description d'erreur
 - Les codes erreur (proviennent de parametres pObjectCodeTo)
Param1 : fichier liste jobs
"""


from DS_GetErrCodeDescription_mod import *
#print("datetime:[" + str(datetime.datetime.today()) + "]")

# dt1999 = datetime.datetime(1999, 1, 1)
# ts1999 = dt1999.timestamp()
# print("ts 1999 :", ts1999)

# print("str2ts :", str2ts("1221594000"))
# print("str2ts :", str2ts("1000000000"))
# print("str2ts :", str2ts("1999999999"))
# print("str2ts :", str2ts("9999999999"))
# print("str2ts :", str2ts("19991231"))
# print("str2ts :", str2ts("20080916")) # ~ 1221594000
# print("str2ts :", str2ts("2008-09-16"))
# print("str2ts :", str2ts("16/09/2008"))
# print("str2ts :", str2ts("1999-12-31"))
# print("str2ts :", str2ts("19991231235959"))
# print("str2ts :", str2ts("19991332246060")) # OSError: [Errno 22] Invalid argument
# print("str2ts :", str2ts("1999abcd"))
# print("str2ts :", str2ts("ef/gh/2008"))
# print("str2ts :", str2ts("16/09/2008 ij:kl:mn"))

# quit()

## 
##  Lire la config
##
ini = lireConfig()


##
##  Determiner derniere utilisation
##
ini['lastrun'] = int(getLastrun())
#log("Dernier traitement:[" + datetime.datetime.fromtimestamp(ini['lastrun']).strftime('%Y-%m-%d %H:%M:%S') + "] TS:[" + str(ini['lastrun']) + "]")
#print("lastrun=[" + str(ini['lastrun']) + "]")
#print(ini)


##
##  Prise en charge de la liste de fichier a traiter
##  dans un dict {path: name: mtime:0 useit:0}
##
dsxListe = getFileList()


## 
## determiner exist, mtime, et useit suivant lastrun
## 
dsxListe = setListeValues(dsxListe, ini['lastrun'])
#log(logListTodoDsxfiles(dsxListe))
#print(dsxListe)


## 
##  Construction d'un dictionnaire job --> version --> objectTo
##
(dJobObjectVersion, dVersion) = secDictJobObjectVersion(ini['fJobObjectVersion'])

# for k in dJobObjectVersion :
    # print(k, TAB, dJobObjectVersion[k])


## 
## Parcourir cette liste pour action
## 

resultats = callParser(dsxListe, dJobObjectVersion, dVersion)

#print("Nbr fichiers DSX :", resultats)