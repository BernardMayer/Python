#!/python

import cgi
import cgitb; cgitb.enable()
import subprocess
import os

#cgi.test()


def buildAction(act, adh) :
    ##  Charger les infos qui permettent d associer cible et faire
    return r"dir c:\temp"

def buildOdbc(act, adh) : 
    ## Construire un DSN pour cet adherent et cette action (MSSQL vs TERADATA)
    odbc_dict = dict()
    # MSSQL global
    odbc_dict['datasource'] = "ISA1_TDA=Teradata"
    
    odbc_dict['driver'] = "c:\\windows\\Sytem32\\SQLSRV32.dll"
    odbc_dict['language'] = ""
    odbc_dict['quotedid'] = "NO"
    odbc_dict['']
    # MSSQL adherent
    
    # Teradata global
    odbc_dict['driver'] = "c:\\progra~1\\Teradata\\Client\\14.10\\ODBC Driver for Teradata nt-x8664\\Lib\\tdata32.dll"
    # Teradata adherent
    
    return retCode
    
form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf8\n")
print(str(form))

print("Action est [" + form.getvalue("valFaire") + "] sur adherent [" + form.getvalue("valCible") + "]<br />") 

##  Faire les verif des 2 parametres
##  TODO

act = buildAction(form.getvalue("valFaire"), form.getvalue("valAction"))

print("<p>action=[" + act + "]</p>")
print("<hr />")

#subprocess.run([r"dir", r"c:\temp"], shell=True) # C:\Windows\System32
#subprocess.call([r"notepad", r"c:\temp\avirer.txt"])
#subprocess.run([r"test.cmd", r"c:\temp"], shell=True)
####    https://python.developpez.com/faq/?page=Generalites#Comment-lancer-un-programme-externe
####    Tout ce qui suit fonctionne
#os.startfile("notepad.exe") # :-) non bloquant
#os.system("notepad.exe") # bloquant
#print(subprocess.run(["notepad.exe", "c:\\temp\\avirer.txt"])) # bloquant, retourne CompletedProcess(args=['notepad.exe', 'c:\\temp\\avirer.txt'], returncode=0) 
#print(subprocess.call(["notepad.exe", "c:\\temp\\avirer.txt"])) # bloquant, retourne 0 a la fermeture de notepad
