;
; Fonction : Demarrage de la CMC dans IE
;
; Quand          Qui   Quoi
; ======== ===  ==== ==========================================
; 5/08/2013     PR   Creation de ce script

#include <file.au3>
#include <Date.au3>
#include <IE.au3>

Dim $URL
Dim $Pwd
Dim $ID_CR
Dim $Duree_sleep

$Pos_point = stringinstr(@Scriptname,".")
$Scriptname_ss_suffix = stringleft(@Scriptname,$Pos_point-1)
; $Fichier_log = "D:\Developpement\BOXI\vbs\Connx_all\" & $Scriptname_ss_suffix & "_" & @Year & @Mon & @Mday & @Hour & @Min & @sec & ".log"

if $CMDLine[0] <> 3 Then
    MsgBox(0, "Erreur", "Pas de parametre passe au script")
	exit
else
	$Serveur_BO = $CMDLine[1]
	$Cle_PWD = $CMDLine[2]
	$VM_BO = $CMDLine[3]
;	$URL = $CMDLine[4]

Endif

$Nom_fichier_ini = "d:\Global\Pwd.ini"
;
; Ouverture du fichier ini
;
$fichier_pwd = FileOpen($Nom_fichier_ini, 0)

If $fichier_pwd = -1 Then
    MsgBox(0, "Erreur", "Fichier '" & $Fichier_pwd & "' impossible à ouvrir")
    Exit
EndIf

While 1

    $ligne_pwd = FileReadLine($fichier_pwd)

    If @error = -1 Then ExitLoop

		$ligne_pwd = StringStripWS($Ligne_pwd,3)

        If StringLen($Ligne_pwd) > 0 Then

            If $Ligne_pwd <> "'" then

; ConsoleWrite("$Ligne_pwd =  " &StringStripWS( $Ligne_pwd,3) & @CR)

				$Array_pwd = Stringsplit($Ligne_pwd,";")

		        If StringStripWS($Array_pwd[1] ,3) = $cle_PWD Then
                    $user = StringStripWS($Array_pwd [3],3)
					$Pwd = StringStripWS($Array_pwd [4],3)

			        ConsoleWrite("$user =  " & $user & @CR)
     			    ConsoleWrite("$Pwd =  " & $Pwd & @CR)
  		        EndIf

			EndIf
        EndIf
WEnd

FileClose($fichier_pwd)
; http://swavpabobj01.zres.ztech/AdminTools/querybuilder/ie.jsp?service=%2FCmcApp%2FApp%2FappService.jsp&cms=swavpabobj01.zres.ztech%3A6400&cmsVisible=false&authType=secEnterprise&authenticationVisible=false&usernameEditable=false&username=ET01354&sm=false&smAuth=secLDAP&sapSSOPrimary=false&sso=false&useLogonToken=false&sessionCookie=true&persistCookies=true&appName=BusinessObjects%20Central%20Management%20Console&prodName=Business%20Objects&appKind=CMC&backContext=%2FCmcApp&backUrlParents=1&backUrl=%2FApp%2Fhome.faces%3FappKind%3DCMC%26service%3D%252FCmcApp%252FApp%252FappService.jsp%26
$URL = "http://" & 	$VM_BO & "/AdminTools/querybuilder/ie.jsp?service=%2FCmcApp%2FApp%2FappService.jsp&cms=" & $Serveur_BO & "%3A6400&cmsVisible=false&authType=secEnterprise&authenticationVisible=false&usernameEditable=false&username=ET01354&sm=false&smAuth=secLDAP&sapSSOPrimary=false&sso=false&useLogonToken=false&sessionCookie=true&persistCookies=true&appName=BusinessObjects%20Central%20Management%20Console&prodName=Business%20Objects&appKind=CMC&backContext=%2FCmcApp&backUrlParents=1&backUrl=%2FApp%2Fhome.faces%3FappKind%3DCMC%26service%3D%252FCmcApp%252FApp%252FappService.jsp%26"

_IECreate($URL)
Sleep(3000)
; BMC Remedy Mid Tier 7.6 - Connexion - Windows Internet Explorer

$oIE = _IEattach("Business Objects Business Intelligence platform - Query Builder")
$hwnd = _IEPropertyGet($oIE, "hwnd")
WinSetState($hwnd, "", @SW_MAXIMIZE) ; Maximize the IE window

Blockinput(1)

Send("{TAB}")
Send( $Pwd )
Send("{TAB}")
Send("{TAB}")
Send("{ENTER}")
sleep(500)

Blockinput(0)
exit
;
; Gestion des erreurs de type COM
;
Func MyErrFunc()
	Consolewrite("ERREUR == Erreur COM Detectee et bypassee")
  ; when COM/Obj error  then only set flag and do nothing
  SetError(1)
  $Erreur_com = True
EndFunc
