""" 
Une (au moins) fonction par action
"""

import os
import sys
#from myApp_mod import *
import myApp_mod

    
def srvBov1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name, ", pour Adh=", Adh)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name + ", pour Adh=" + Adh)
    print("BO-User=", dIni['dAdherents'][Adh]['BO-User'], "BO-Pwd=", dIni['dAdherents'][Adh]['BO-Pwd'])

    
def srvBov2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)


def cliSqlv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def cliSqlv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def deski2v1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    ##  Construire un DSN ODBC

    
def deski2v2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)
    ##  Construire un DSN ODBC

    
def deski3v1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def deski3v2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def designv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def designv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def cmcv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def cmcv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def infoviewv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def infoviewv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def qBuildv1(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)

    
def qBuildv2(dIni, Adh) : 
    """ ACTIONBO  """
    """  """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
    myApp_mod.alert("TODO " + sys._getframe().f_code.co_name)


def dirUniv(dIni, Adh = None) :
    """ ACTION_BO_DIR_UNIVERS    """
    """ Recuperer dans le fichier ini le repertoire cible    """
    print("RUN la fonction=", sys._getframe().f_code.co_name)
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
        
    #print("cmd=", bo_dir_cmd + " " + bo_dir_univ)
    os.system(bo_dir_cmd + " " + bo_dir_univ)
    
    
def dirRapp(dIni, Adh = None) : 
    """ ACTION_BO_DIR_RAPP    """
    """ Recuperer dans le fichier ini le repertoire cible    """
    print("nom de la fonction=", sys._getframe().f_code.co_name)
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
        
    #print("cmd=", bo_dir_cmd + " " + bo_dir_rapp)
    os.system(bo_dir_cmd + " " + bo_dir_rapp)