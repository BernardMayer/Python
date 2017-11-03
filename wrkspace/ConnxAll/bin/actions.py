""" 
Une (au moins) fonction par action
"""

import os
import sys
import subprocess
#from myApp_mod import *
import myApp_mod


    
def srvBov1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name, ", pour Adh=", Adh)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name + ", pour Adh=" + Adh)
    # print("BO-User=", dIni['dAdherents'][Adh]['BO-User'], "BO-Pwd=", dIni['dAdherents'][Adh]['BO-Pwd'])
    exe = dIni['objCfg']['srvBov1']['srvBov1_exe']
    d = dIni['dAdherents'][Adh]['MS-Domain'].upper() # ZGIE|YGIE
    h = dIni['dAdherents'][Adh]['BO-Host']
    u = None
    p = None
    if (d == 'ZRES') :
        u = dIni['objCfg']['srvBov1']['srvBov1_ZGIE_user']
        p = dIni['objCfg']['srvBov1']['srvBov1_ZGIE_pwd']
    if (d == 'YRES') :
        u = dIni['objCfg']['srvBov1']['srvBov1_YGIE_user']
        p = dIni['objCfg']['srvBov1']['srvBov1_YGIE_pwd']
    # u = None
    # print("d=", d, ", u=", u, ", p=", p)
    
    try :
        # if (u is None or p is None) :
            # raise ValueError("Pb avec user et mot de passe pour MS-Domain")
        #cmd = '"' + exe + '"' + " /v:" + h + " /u:" + u + " /p:" + p 
        cmd = '"' + exe + '"' + " /v:" + h + " /u:" + u + " /p:" + p + " /domain:" + d + " /drives:fixed,-u: /max /title:BO-" + Adh
        #cmd = "toto"
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        #os.system(cmd)
        #subprocess.run([..., ...])  # doesn't capture output
        # subprocess.Popen(cmd) # lancer genre drop and forget
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [srvBov1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [srvBov1] du fichier de ini/cfg")
    
def srvBov2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)


def cliSqlv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    
    # import subprocess

    # etcd = subprocess.Popen('etcd') # continue immediately
    # next_cmd_returncode = subprocess.call('next_cmd') # wait for it
    # # ... run more python here ...
    # etcd.terminate() 
    # etcd.wait()
    
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    try :
        # Construire la ligne de commande, a partir des infos actions, et adherent
        cliSqlv1_exe = dIni['objCfg']['cliSqlv1']['cliSqlv1_exe']
        print("dAdherents=\n", dIni['dAdherents'][Adh])
        cliSqlv1_host = dIni['dAdherents'][Adh]['DBv1-Host']
        cliSqlv1_base = dIni['dAdherents'][Adh]['DBv1-Base']
        cliSqlv1_user = dIni['dAdherents'][Adh]['DBv1-User']
        cliSqlv1_pwd  = dIni['dAdherents'][Adh]['DBv1-Pwd']
        #cmd = '"' + infoviewv1_exe + " http://" + infoviewv1_host + "/InfoViewApp/logon.jsp" + '"' # &username=ETH0589 # &authType=secEnterprise
        # sCMD  = "C:\Program Files (x86)\Microsoft SQL Server\100\Tools\Binn\VSShell\Common7\IDE\Ssms.exe" -s REP10-BOBJSQL\REP10 -d DREP10DTWH01J -U CO_REP10BOBJU_DBC -P adminBO -nosplash
        # RUN de ["C:\Program Files (x86)\Microsoft SQL Server\100\Tools\Binn\VSShell\Common7\IDE\Ssms.exe" -s REp10bobju_dbc -U CO_REP10BOBJU_DBC -PadminBO -d dREp10dtwh01j]
        cmd = '"' + cliSqlv1_exe + '"' + " -s " + cliSqlv1_host + " -U " + cliSqlv1_user + " -P " + cliSqlv1_pwd + " -d " + cliSqlv1_base + "  -nosplash"
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        #os.system(cmd)
        #subprocess.run([..., ...])  # doesn't capture output
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [cliSqlv1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [cliSqlv1] du fichier de ini/cfg")

    
def cliSqlv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    try :
        # print("dAdherents=\n", dIni['dAdherents'][Adh])
        cliSqlv2_host = dIni['dAdherents'][Adh]['DB-Host']
        cliSqlv2_base = dIni['dAdherents'][Adh]['DB-Base']
        cliSqlv2_user = dIni['dAdherents'][Adh]['DB-User']
        cliSqlv2_pwd  = dIni['dAdherents'][Adh]['DB-Pwd']
        
        # Construire un ODBC avec un nom -PARTICULIER- a la Caisse, 
        # pour ne pas faire de collision avec le DSN de deski2tiers
        cliSqlv2_DSN  = dIni['dAdherents'][Adh]['AdhId'] + dIni['dAdherents'][Adh]['AdhNum'] + "v2"
        
        # La clef ODBC a fabriquer pour cet Adherent
        keyVal = 'Software\\ODBC\\ODBC.INI\\' + cliSqlv2_DSN
        # print("keyVal =", keyVal)
        
        # L'ensemble des valeurs liees a la clef sont sous forme de dictionnaire
        clefs = dict()
        ##  Valeurs specifiques Teradata a l'Adherent
        clefs['DateTimeFormat'] = "III" #"AAA"
        clefs['DBCName'] = dIni['dAdherents'][Adh]['DB-Host']
        clefs['Driver'] = dIni['objCfg']['cliSqlv2']['cliSqlv2_odbc_drv']
        clefs['SessionMode'] = "Teradata"
        clefs['Username'] = dIni['dAdherents'][Adh]['DB-User']
        clefs['DefaultDatabase'] = "VZUTB0REST_ADH_CPDT_BO_0"
        clefs['Database'] = "VZUTB0REST_ADH_CPDT_BO_0"
        clefs['MechanismName'] = "TD2" #"TD2     "
        clefs['DsnOptions'] = "1010101000000010000000111"
        clefs['DontUseHelpDatabase'] = "Yes"
        clefs['MaxRespSize'] = "1048575"
        clefs['LoginTimeout'] = "20"
        clefs['CharacterSet'] = "UTF8"
        #clefs['Password'] = "pXgB2ywofgp1lW9uyXGY"
        #clefs['Password_X'] = ""
        clefs['MechanismKey'] = ""
        clefs['AccountString'] = ""
        clefs['Description'] = "Connexion v2 teradata pour Adherent " + dIni['dAdherents'][Adh]['AdhLib']
        # clefs[''] = 

        # print("Le DSN serait :", cliSqlv2_DSN, "suivi de :\nDSN=", cliSqlv2_DSN, " host=", cliSqlv2_host, " user=", cliSqlv2_user, " pwd =", cliSqlv2_pwd)
        # print("keyVal =", keyVal)
        #print(clefs)
        myApp_mod.build_dsn(keyVal, clefs)
        
        ## Reference de la clef de l'Adherent dans ODBC.INI\ODBC Data Sources
        keyVal = 'Software\\ODBC\\ODBC.INI\\ODBC Data Sources'
        clefs = dict()
        clefs[cliSqlv2_DSN] = "Teradata"
        myApp_mod.build_dsn(keyVal, clefs)
        
        # cliSqlv2_DSN = "ZUTB1"
        # cliSqlv2_user = "CO_ZUTB1META_SLUD"
        # cliSqlv2_pwd  = "qrUyho9eAz0R4QCJJKOo"
        # cliSqlv2_base = "DZUTB1DTWH_DTA_0"
        
        # Construire la ligne de commande, a partir des infos actions, et adherent
        # ! il n'y a pas d'espace entre DSN, \user, et \pwd !
        cliSqlv2_exe = dIni['objCfg']['cliSqlv2']['cliSqlv2_exe']
        #cmd = '"' + infoviewv1_exe + " http://" + infoviewv1_host + "/InfoViewApp/logon.jsp" + '"' # &username=ETH0589 # &authType=secEnterprise
        #cmd = '"' + cliSqlv2_exe + '"' + " -s " + cliSqlv2_host + " -U " + cliSqlv1_user + " -P " + cliSqlv1_pwd + " -d " + cliSqlv1_base + "  -nosplash"
        cmd = '"' + cliSqlv2_exe + '"' + " -c " + cliSqlv2_DSN + "\\" + cliSqlv2_user + "\\" + cliSqlv2_pwd + " -db " + cliSqlv2_base
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        #os.system(cmd)
        #subprocess.run([..., ...])  # doesn't capture output
        # subprocess.Popen(cmd) # lancer genre drop and forget
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [cliSqlv2] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [cliSqlv2] du fichier de ini/cfg")

            
def deski2v1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    
    #'p:\Documents\My Business Objects Documents\LocData/swmaPDEDVR01_zres_ztech.intranet'
    try :
        # print("dAdherents=\n", dIni['dAdherents'][Adh])
        deski2v1_host = dIni['dAdherents'][Adh]['DBv1-Host']
        deski2v1_base = dIni['dAdherents'][Adh]['DBv1-Base']
        deski2v1_baseAudit = dIni['dAdherents'][Adh]['DBv1-BaseAudit']
        deski2v1_user = dIni['dAdherents'][Adh]['DBv1-User']
        deski2v1_pwd  = dIni['dAdherents'][Adh]['DBv1-Pwd']
        
        # Construire un ODBC avec un nom -PARTICULIER- a la Caisse, 
        # pour ne pas faire de collision avec le DSN de deski2tiers
        #cliSqlv2_DSN  = dIni['dAdherents'][Adh]['AdhId'] + dIni['dAdherents'][Adh]['AdhNum'] + "v1"
        
        ##  La clef ODBCa fabriquer pour cet Adherent, pour les donnees 
        # L'ensemble des valeurs liees a la clef sont sous forme de dictionnaire
        clefs = dict()    
        clefs['Database'] = deski2v1_base
        clefs['Description'] = "Connexion v1 MS-Sql pour Adherent " + dIni['dAdherents'][Adh]['AdhLib']
        clefs['Driver'] = dIni['objCfg']['deski2v1']['deski2v1_odbc_drv']
        clefs['Server'] = deski2v1_host
        clefs['Trusted_Connection'] = "NO"
        clefs['Language'] = "us_english"
        clefs['QuotedId'] = "NO"
        # clefs[''] = 
        # clefs[''] = 
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ISA1_SQL', clefs)

        ##  La clef ODBC a fabriquer pour cet Adherent, pour l'audit (seule la DB change)
        # Les autres clefs sont conservees, seule la base est changee
        clefs['Database'] = deski2v1_baseAudit
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ISA1_BOAuditXi', clefs)
    
        clefs = dict()
        clefs['ISA1_SQL'] = "SQL Server"
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ODBC Data Sources', clefs)
        
        clefs = dict()
        clefs['ISA1_BOAuditXi'] = "SQL Server"
        myApp_mod.build_dsn('ISA1_BOAuditXi', clefs)
        
        # Creation fichier locdata
        w = dIni['objCfg']['deski2v1']['deski2v1_locdata_path']
        h = dIni['dAdherents'][Adh]['BO-Host']
        u = dIni['dAdherents'][Adh]['BO-User']
        myApp_mod.build_locdata_2tiers(w, h, u)
        
        deski2v1_exe = dIni['objCfg']['deski2v1']['deski2v1_exe']
        cmd = '"' + deski2v1_exe + '"' + " -system " + dIni['dAdherents'][Adh]['BO-Host'] + " -User " + dIni['dAdherents'][Adh]['BO-User'] + " -Pass " + dIni['dAdherents'][Adh]['BO-Pwd'] + ' -auth Enterprise'
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        #os.system(cmd)
        #subprocess.run([..., ...])  # doesn't capture output
        # subprocess.Popen(cmd) # lancer genre drop and forget
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [deski2v1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [deski2v1] du fichier de ini/cfg")

            
def deski2v2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    ##  Construire un DSN ODBC
    # "C:\LOGICIELS\Business Objects\BusinessObjects Enterprise 12.0\win32_x86\busobj.exe" -system swrePDEDVR01.zres.ztech -User ETH0589 -Pass EvelyneLauBen -auth "Enterprise"

    #'p:\Documents\My Business Objects Documents\LocData/swmaPDEDVR01_zres_ztech.intranet'
    try :
        # print("dAdherents=\n", dIni['dAdherents'][Adh])
        deski2v2_host = dIni['dAdherents'][Adh]['DB-Host']
        deski2v2_base = dIni['dAdherents'][Adh]['DB-Base']
        deski2v2_user = dIni['dAdherents'][Adh]['DB-User']
        deski2v2_pwd  = dIni['dAdherents'][Adh]['DB-Pwd']
        
        # Creation fichier locdata
        w = dIni['objCfg']['deski2v2']['deski2v2_locdata_path']
        h = dIni['dAdherents'][Adh]['BO-Host']
        u = dIni['dAdherents'][Adh]['BO-User']
        myApp_mod.build_locdata_2tiers(w, h, u)
        
        # Construire un ODBC avec un nom -PARTICULIER- a la Caisse, 
        # pour ne pas faire de collision avec le DSN de deski2tiers
        # deski2v2_DSN = dIni['dAdherents'][Adh]['AdhId'] + dIni['dAdherents'][Adh]['AdhNum'] + "v2"
        deski2v2_DSN = "ISA1_TDA"
        
        # La clef ODBC a fabriquer pour cet Adherent, pour les donnees
        
        # L'ensemble des valeurs liees a la clef sont sous forme de dictionnaire
        clefs = dict()
        ##  Valeurs specifiques Teradata a l'Adherent
        clefs['DateTimeFormat'] = "III" #"AAA"
        clefs['DBCName'] = dIni['dAdherents'][Adh]['DB-Host']
        clefs['Driver'] = dIni['objCfg']['deski2v2']['deski2v2_odbc_drv']
        clefs['SessionMode'] = "Teradata"
        clefs['Username'] = dIni['dAdherents'][Adh]['DB-User']
        clefs['DefaultDatabase'] = "VZUTB0REST_ADH_CPDT_BO_0"
        clefs['Database'] = "VZUTB0REST_ADH_CPDT_BO_0"
        clefs['MechanismName'] = "TD2" #"TD2     "
        clefs['DsnOptions'] = "1010101000000010000000111"
        clefs['DontUseHelpDatabase'] = "Yes"
        clefs['MaxRespSize'] = "1048575"
        clefs['LoginTimeout'] = "20"
        clefs['CharacterSet'] = "UTF8"
        #clefs['Password'] = "pXgB2ywofgp1lW9uyXGY"
        #clefs['Password_X'] = ""
        clefs['MechanismKey'] = ""
        clefs['AccountString'] = ""
        clefs['Description'] = "Connexion v2 teradata pour Adherent " + dIni['dAdherents'][Adh]['AdhLib']
        #print(clefs)
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ISA1_TDA', clefs)
        
        ## Pour l'audit
        #?
        
        ## Reference de la clef de l'Adherent dans ODBC.INI\ODBC Data Sources
        clefs = dict()
        clefs['ISA1_TDA'] = "Teradata"
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ODBC Data Sources', clefs)
    
        deski2v2_exe = dIni['objCfg']['deski2v2']['deski2v2_exe']
        cmd = '"' + deski2v2_exe + '"' + " -system " + dIni['dAdherents'][Adh]['BO-Host'] + " -User " + dIni['dAdherents'][Adh]['BO-User'] + " -Pass " + dIni['dAdherents'][Adh]['BO-Pwd'] + ' -auth Enterprise'
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        #os.system(cmd)
        #subprocess.run([..., ...])  # doesn't capture output
        # subprocess.Popen(cmd) # lancer genre drop and forget
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [deski2v2] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [deski2v2] du fichier de ini/cfg")

    
def deski3v1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    # Nom_locdata =  'p:\Documents\My Business Objects Documents\LocData/swrePDEDVR01_zres_ztech@6400_j2ee.extranet'
    # "C:\LOGICIELS\Business Objects\BusinessObjects Enterprise 12.0\win32_x86\busobj.exe" -system "swrePDEDVR01.zres.ztech:6400 (J2EE Portal)" -User ETH0589 -Pass EvelyneLauBen -auth "Enterprise"
    
    try : 
        deski3v1_host = dIni['dAdherents'][Adh]['DB-Host']
        deski3v1_base = dIni['dAdherents'][Adh]['DB-Base']
        deski3v1_user = dIni['dAdherents'][Adh]['DB-User']
        deski3v1_pwd  = dIni['dAdherents'][Adh]['DB-Pwd']
            
        # Creation fichier locdata
        w = dIni['objCfg']['deski3v1']['deski3v1_locdata_path']
        h = dIni['dAdherents'][Adh]['BO-Host']
        u = dIni['dAdherents'][Adh]['BO-User']
        myApp_mod.build_locdata_3tiers(w, h, u)
        
        deski3v1_exe = dIni['objCfg']['deski3v1']['deski3v1_exe']
        cmd = '"' + deski3v1_exe + '"' + " -system " + '"' + dIni['dAdherents'][Adh]['BO-Host'] + ":6400 (J2EE Portal)" + '"' + " -User " + dIni['dAdherents'][Adh]['BO-User'] + " -Pass " + dIni['dAdherents'][Adh]['BO-Pwd'] + ' -auth Enterprise'
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
            #os.system(cmd)
            #subprocess.run([..., ...])  # doesn't capture output
            # subprocess.Popen(cmd) # lancer genre drop and forget
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [deski2v2] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [deski2v2] du fichier de ini/cfg")
    
    
def deski3v2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def designv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    try :
        # print("dAdherents=\n", dIni['dAdherents'][Adh])
        designv1_host = dIni['dAdherents'][Adh]['DBv1-Host']
        designv1_base = dIni['dAdherents'][Adh]['DBv1-Base']
        designv1_baseAudit = dIni['dAdherents'][Adh]['DBv1-BaseAudit']
        designv1_user = dIni['dAdherents'][Adh]['DBv1-User']
        designv1_pwd  = dIni['dAdherents'][Adh]['DBv1-Pwd']
        
        # Construire un ODBC avec un nom -PARTICULIER- a la Caisse, 
        # pour ne pas faire de collision avec le DSN de deski2tiers
        #cliSqlv2_DSN  = dIni['dAdherents'][Adh]['AdhId'] + dIni['dAdherents'][Adh]['AdhNum'] + "v1"
        
        ##  La clef ODBCa fabriquer pour cet Adherent, pour les donnees 
        # L'ensemble des valeurs liees a la clef sont sous forme de dictionnaire
        clefs = dict()    
        clefs['Database'] = designv1_base
        clefs['Description'] = "Connexion v1 MS-Sql pour Adherent " + dIni['dAdherents'][Adh]['AdhLib']
        clefs['Driver'] = dIni['objCfg']['designv1']['designv1_odbc_drv']
        clefs['Server'] = designv1_host
        clefs['Trusted_Connection'] = "NO"
        clefs['Language'] = "us_english"
        clefs['QuotedId'] = "NO"
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ISA1_SQL', clefs)

        ##  La clef ODBC a fabriquer pour cet Adherent, pour l'audit (seule la DB change)
        # Les autres clefs sont conservees, seule la base est changee
        clefs['Database'] = designv1_baseAudit
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ISA1_BOAuditXi', clefs)
    
        clefs = dict()
        clefs['ISA1_SQL'] = "SQL Server"
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ODBC Data Sources', clefs)
        
        clefs = dict()
        clefs['ISA1_BOAuditXi'] = "SQL Server"
        myApp_mod.build_dsn('Software\\ODBC\\ODBC.INI\\ODBC Data Sources', clefs)
        
        # Creation fichier locdata
        w = dIni['objCfg']['designv1']['designv1_locdata_path']
        h = dIni['dAdherents'][Adh]['BO-Host']
        u = dIni['dAdherents'][Adh]['BO-User']
        myApp_mod.build_locdata_2tiers(w, h, u)
        
        designv1_exe = dIni['objCfg']['designv1']['designv1_exe']
        cmd = '"' + designv1_exe + '"' + " -system " + dIni['dAdherents'][Adh]['BO-Host'] + " -User " + dIni['dAdherents'][Adh]['BO-User'] + " -Pass " + dIni['dAdherents'][Adh]['BO-Pwd'] + ' -auth Enterprise'
        # cmd = "TOTO"
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        #os.system(cmd)
        #subprocess.run([..., ...])  # doesn't capture output
        # subprocess.Popen(cmd) # lancer genre drop and forget
        subprocess.Popen(cmd)
    except :
        log("ERREUR : Verifier les infos Adherents et la section [designv1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier les infos Adherents et la section [designv1] du fichier de ini/cfg")

 
def designv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def cmcv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    try :
        # Construire la ligne de commande, a partir des infos actions, et adherent
        cmcv1_exe = dIni['objCfg']['cmcv1']['cmcv1_exe']
        #print("dAdherents=\n", dIni['dAdherents'][Adh]['BO-Host'])
        cmcv1_host = dIni['dAdherents'][Adh]['BO-Host']
        # TODO ?authType=secEnterprise&username=ETH0589
        cmcv1_user = dIni['dAdherents'][Adh]['BO-User']
        cmcv1_pwd  = dIni['dAdherents'][Adh]['BO-Pwd']
        cmd = '"' + cmcv1_exe + " http://" + cmcv1_host + "/CmcApp/logon.faces" + '"' # &username=ETH0589 # &authType=secEnterprise
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        os.system(cmd)
    except :
        log("ERREUR : Verifier BO-Host dans les infos Adherents, et cmcv1_exe = dans la section [cmcv1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier BO-Host dans les infos Adherents, et cmcv1_exe = dans la section [cmcv1] du fichier de ini/cfg")

            
def cmcv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def infoviewv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    try :
        # Construire la ligne de commande, a partir des infos actions, et adherent
        infoviewv1_exe = dIni['objCfg']['infoviewv1']['infoviewv1_exe']
        #print("dAdherents=\n", dIni['dAdherents'][Adh]['BO-Host'])
        infoviewv1_host = dIni['dAdherents'][Adh]['BO-Host']
        # TODO ?authType=secEnterprise&username=ETH0589
        infoviewv1_user = dIni['dAdherents'][Adh]['BO-User']
        infoviewv1_pwd  = dIni['dAdherents'][Adh]['BO-Pwd']
        cmd = '"' + infoviewv1_exe + " http://" + infoviewv1_host + "/InfoViewApp/logon.jsp" + '"' # &username=ETH0589 # &authType=secEnterprise
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        os.system(cmd)
    except :
        log("ERREUR : Verifier BO-Host dans les infos Adherents, et infoviewv1_exe = dans la section [infoviewv1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier BO-Host dans les infos Adherents, et infoviewv1_exe = dans la section [infoviewv1] du fichier de ini/cfg")

    
def infoviewv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def qBuildv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    # print("RUN la fonction=", sys._getframe().f_code.co_name)
    # myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    # 
    try :
        # Construire la ligne de commande, a partir des infos actions, et adherent
        qBuildv1_exe = dIni['objCfg']['qBuildv1']['qBuildv1_exe']
        #print("dAdherents=\n", dIni['dAdherents'][Adh]['BO-Host'])
        qBuildv1_host = dIni['dAdherents'][Adh]['BO-Host']
        # TODO ?authType=secEnterprise&username=ETH0589
        qBuildv1_user = dIni['dAdherents'][Adh]['BO-User']
        qBuildv1_pwd  = dIni['dAdherents'][Adh]['BO-Pwd']
        cmd = '"' + qBuildv1_exe + " http://" + qBuildv1_host + "/AdminTools/querybuilder/logonform.jsp" + '"' # &username=ETH0589 # &authType=secEnterprise
        if (dIni['verbose']) : 
            print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + cmd + "]")
        os.system(cmd)
    except :
        log("ERREUR : Verifier BO-Host dans les infos Adherents, et qBuildv1_exe = dans la section [qBuildv1] du fichier de ini/cfg")
        if (dIni['verbose']) : 
            print("ERREUR : Verifier BO-Host dans les infos Adherents, et qBuildv1_exe = dans la section [qBuildv1] du fichier de ini/cfg")

            
def qBuildv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)


def dirUniv(dIni, Adh = None) :
    """ ACTION_BO_DIR_UNIVERS    """
    """ Recuperer dans le fichier ini le repertoire cible    """
    bo_dir_section = sys._getframe().f_code.co_name
    bo_dir_cmd_section  = "bo_dir_cmd"
    bo_dir_univ_section = "bo_dir_univ"
    try :
        ##  La section relative a cette fonction
        section = dIni['objCfg'][bo_dir_section]
    except :
        myApp_mod.log("ERREUR : Il n'y a pas de section [" + bo_dir_section + "] dans le fichier de configuration")
        myApp_mod.alert("ERREUR : Il n'y a pas de section [" + bo_dir_section + "] dans le fichier de configuration")
        if (dIni['verbose']) : 
            print("ERREUR : Il n'y a pas de section [" + bo_dir_section + "] dans le fichier de configuration")
    else :
        try : 
            ## L'option 1 
            bo_dir_cmd = dIni['objCfg'][bo_dir_section][bo_dir_cmd_section]
        except :
            myApp_mod.alert("ERREUR : il manque l'option [" + bo_dir_cmd_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
            myApp_mod.log("ERREUR : il manque l'option [" + bo_dir_cmd_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
            if (dIni['verbose']) :
                print("ERREUR : il manque l'option [" + bo_dir_cmd_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")        
        else : 
            try : 
                ##  L'option 2
                bo_dir_univ = dIni['objCfg'][bo_dir_section][bo_dir_univ_section] 
            except : 
                myApp_mod.alert("ERREUR : il manque l'option [" + bo_dir_univ_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
                myApp_mod.log("ERREUR : il manque l'option [" + bo_dir_univ_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
                if (dIni['verbose']) :
                    print("ERREUR : il manque l'option [" + bo_dir_univ_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")   

    if (dIni['verbose']) : 
        print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + bo_dir_cmd + " " + bo_dir_univ + "]")
    os.system(bo_dir_cmd + " " + bo_dir_univ)
    
    
def dirRapp(dIni, Adh = None) : 
    """ ACTION_BO_DIR_RAPP    """
    """ Recuperer dans le fichier ini le repertoire cible    """
    bo_dir_section = sys._getframe().f_code.co_name
    bo_dir_cmd_section  = "bo_dir_cmd"
    bo_dir_rapp_section = "bo_dir_rapp"
    try :
        ##  La section relative a cette fonction
        section = dIni['objCfg'][bo_dir_section]
    except :
        myApp_mod.log("ERREUR : Il n'y a pas de section [" + bo_dir_section + "] dans le fichier de configuration")
        myApp_mod.alert("ERREUR : Il n'y a pas de section [" + bo_dir_section + "] dans le fichier de configuration")
        if (dIni['verbose']) : 
            print("ERREUR : Il n'y a pas de section [" + bo_dir_section + "] dans le fichier de configuration")
    else :
        try : 
            ## L'option 1 
            bo_dir_cmd = dIni['objCfg'][bo_dir_section][bo_dir_cmd_section]
        except :
            myApp_mod.alert("ERREUR : il manque l'option [" + bo_dir_cmd_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
            myApp_mod.log("ERREUR : il manque l'option [" + bo_dir_cmd_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
            if (dIni['verbose']) :
                print("ERREUR : il manque l'option [" + bo_dir_cmd_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")        
        else : 
            try : 
                ##  L'option 2
                bo_dir_rapp = dIni['objCfg'][bo_dir_section][bo_dir_rapp_section] 
                print("BINGO")
                print("la config de la fonction=", dIni['objCfg'][bo_dir_section][bo_dir_rapp_section])
            except : 
                myApp_mod.alert("ERREUR : il manque l'option [" + bo_dir_rapp_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
                myApp_mod.log("ERREUR : il manque l'option [" + bo_dir_rapp_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")
                if (dIni['verbose']) :
                    print("ERREUR : il manque l'option [" + bo_dir_rapp_section + "] dans la section [" + bo_dir_section + "] du fichier de configuration")   

    if (dIni['verbose']) : 
        print("Fonction " + sys._getframe().f_code.co_name + " : RUN de [" + bo_dir_cmd + " " + bo_dir_rapp + "]")
    os.system(bo_dir_cmd + " " + bo_dir_rapp)