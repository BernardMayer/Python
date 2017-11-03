' ---------------------------------------------------------------------
' Script de lancement d'application avec RUNAS
' Syntaxe identique à RUNAS mais avec en plus passage du mot de passe 
'
' Syntaxe:
' XRUNAS [/profile] [/env] [/netonly] /user:<NomUtilisateur> /pwd:<password> programme
'   /profile        si le profil de l'utilisateur doit être chargé
'   /env            pour utiliser l'environnement en cours à la place de
'                   celui de l'utilisateur.
'   /netonly        à utiliser si les informations d'identification spécifiées
'                   sont pour l'accès à distance seulement.
'   /user           <NomUtilisateur> sous la forme UTILISATEUR@DOMAINE
'                   ou DOMAINE\UTILISATEUR
'	/pwd			<password> : le mot de passe
'   programme       ligne de commande pour EXE. 
'
'
' JC BELLAMY © 2002
' ---------------------------------------------------------------------
Const SW_HIDE=0
Const SW_SHOWNORMAL=1 
Const SW_SHOWMIN=2 
Const Duree_sleep=100

Dim shell, args, fso, erreur

Set net   = Wscript.CreateObject("WScript.Network")
Set shell = WScript.CreateObject("WScript.Shell")
Set fso   = WScript.CreateObject("Scripting.FileSystemObject")
Set args  = Wscript.Arguments
nbargs=args.count

Title=shell.ExpandEnvironmentStrings("%systemroot%") & "\system32\runas.exe"
If not fso.FileExists(Title) Then 
	msg="Commande " & Title & " non trouvée" & VBCRLF
	msg=msg & "Ce script ne fonctionne que sous Windows 2000 et au delà" & VBCRLF
	wscript.echo msg
	wscript.quit
	End If

If nbargs=0 or testarg("?") or testarg("h") Then Syntaxe ""
defmoteur="cscript"
TestHost true

erreur=false
profile=""
env=""
netonly=""
If testarg("profile") Then profile="/profile "
If testarg("env") Then env="/env "
If testarg("netonly") Then netonly="/netonly "
If testarg("user:") Then user=getarg("user:") else MsgErr("Utilisateur absent")
If testarg("pwd:") Then pwd=getarg("pwd:") else MsgErr("Mot de passe absent")
testprog=false
For i = 0 To nbargs-1
	curarg=args(i)
	If left(curarg,1)<>"/" and left(curarg,1)<>"-" Then 
		programme=curarg
		testprog=true
		exit for
		End If
	Next
If not testprog then MsgErr("Programme absent")
If erreur Then Syntaxe "erreur"
' wscript.echo "Programme =  "  & Programme 

Commande="runas " & profile & env & netonly & "/user:" & user & " """ & programme & """"

' shell.run Commande,SW_SHOWNORMAL
shell.run Commande,SW_SHOWMIN
Title=shell.ExpandEnvironmentStrings("%systemroot%") & "\system32\runas.exe"
shell.AppActivate Title
WScript.Sleep Duree_sleep
shell.SendKeys pwd & "~"
Wscript.quit
'--------------------------------------------------------------------
Function testarg(param)
testarg=false
For i = 0 To nbargs-1
	curarg=lcase(args(i))
	If left(curarg,1)="/" or left(curarg,1)="-" Then
		If mid(curarg,2,len(param))=param Then
			testarg=true
			exit function
			End If
		End If
	Next
End Function
'--------------------------------------------------------------------
Function getarg(param)
getarg=""
For i = 0 To nbargs-1
	curarg=lcase(args(i))
	If left(curarg,1)="/" or left(curarg,1)="-" Then
		If mid(curarg,2,len(param))=param Then
			getarg=mid(args(i),2+len(param))
			exit function
			End If
		End If
	Next
End Function
'--------------------------------------------------------------------
Sub MsgErr(msg)
wscript.echo "Erreur : " & msg
erreur=true
End Sub
'--------------------------------------------------------------------
' Sous programme de test du moteur
Sub TestHost(force)
dim rep
strappli=lcase(Wscript.ScriptFullName)
strFullName =lcase(WScript.FullName)
i=InStr(1,strFullName,".exe",1)
j=InStrRev(strFullName,"\",i,1)
strCommand=Mid(strFullName,j+1,i-j-1)
if strCommand<>"cscript" then
	If force then 
		Init="Ce script doit être lancé avec CSCRIPT"
	Else
		Init="Il est préférable de lancer ce script avec CSCRIPT"
		End If
	rep=MsgBox(Init & VBCRLF & _
	"Cela peut être rendu permanent avec la commande" & VBCRLF & _
	"cscript //H:CScript //S /Nologo" & VBCRLF & _
	"Voulez-vous que ce soit fait automatiquement?", _
	vbYesNo + vbQuestion,strappli)
	if rep=vbYes  then 
		nomcmd="setscript.bat"
		Set ficcmd = fso.CreateTextFile(nomcmd)
		ficcmd.writeline "@echo off"
		ficcmd.writeline "cscript //H:CScript //S /Nologo"
		ficcmd.writeline "pause"
		params=""
		For i = 0 To nbargs-1 
			params=params & " " & args(i)
			next
		ficcmd.writeline chr(34) & strappli & chr(34) & params
		ficcmd.writeline "pause"
		ficcmd.close
		shell.Run nomcmd, SW_SHOWNORMAL,true
		force=true
		end if
    If force then WScript.Quit
	end if
end sub
'--------------------------------------------------------------------
Sub Syntaxe(info)
If info="" Then
	msg=      "Script VBS de lancement d'application avec RUNAS" & VBCRLF
	msg=msg & "avec passage en paramètre du mot de passe" & VBCRLF & VBCRLF
	msg=msg & "JC BELLAMY © 2002" & VBCRLF 
	End If
msg=msg & "------------------------------------------" & VBCRLF
msg=msg & "Syntaxe : " & VBCRLF
msg=msg & " XRUNAS [/profile] [/env] [/netonly] /user:<compte> /pwd:<password> commande" & VBCRLF
msg=msg & "Paramètres :" & VBCRLF 
msg=msg & " /profile   si le profil de l'utilisateur doit être chargé" & VBCRLF
msg=msg & " /env       pour utiliser l'environnement en cours à la place de" & VBCRLF
msg=msg & "            celui de l'utilisateur." & VBCRLF
msg=msg & " /netonly   à utiliser si les informations d'identification spécifiées" & VBCRLF
msg=msg & "            sont pour l'accès à distance seulement." & VBCRLF
msg=msg & " /user      <compte> sous la forme UTILISATEUR@DOMAINE" & VBCRLF
msg=msg & "            ou UTILISATEUR ou DOMAINE\UTILISATEUR" & VBCRLF 
msg=msg & " /pwd       <password> : le mot de passe" & VBCRLF 
msg=msg & "            NB : sensible à la casse (minuscules/majuscules)" & VBCRLF
msg=msg & " commande   commande à exécuter" & VBCRLF & VBCRLF 
msg=msg & "Exemples :" & VBCRLF
msg=msg & "> xrunas /profile /user:administrateur /pwd:toto cmd" & VBCRLF
msg=msg & "> xrunas /profile /env /user:MonDomaine\admin /pwd:truc ""mmc %windir%\system32\dsa.msc"" " & VBCRLF
msg=msg & "> xrunas /env /user:utilisateur@domaine.microsoft.com /pwd:bill ""notepad \""Fichier.txt\"" " & VBCRLF & VBCRLF
msg=msg & "NB: vu que le mot de passe est visible, ce script ne doit être utilisé" & VBCRLF
msg=msg & "    qu'en des circonstances bien particulières!" & VBCRLF 
msg=msg & "    USER@DOMAIN n'est pas compatible avec /netonly." & VBCRLF & VBCRLF
wscript.echo msg
wscript.quit
End Sub
' -------------------------------------

