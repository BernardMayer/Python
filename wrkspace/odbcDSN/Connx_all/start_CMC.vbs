Public IE

Dim CMS, UserID, Password, Report, Authorization, Strg
Dim frames
Dim frame

' ****************************************************************
'
' Initialisation des traitements
'
' ****************************************************************
'
' Récupération du no de lot de réalisation
'
If Wscript.Arguments.Count <> 4 Then

    wscript.echo Date & " - " & Time & " == ERREUR  =  "
    wscript.echo Date & " - " & Time & " == ERREUR  =  No du lot de réalisation non passé"
    wscript.echo Date & " - " & Time & " == ERREUR  =  "
    wscript.echo Date & " - " & Time & " == ERREUR  =  La syntaxe de la commande est :"
    wscript.echo Date & " - " & Time & " == ERREUR  =        start_CMC.vbs <Nom_CR> <Nom User> <Password> <Type authentification>"
    wscript.echo Date & " - " & Time & " == ERREUR  =  "

    wscript.quit(1)
Else
   cmsName = Wscript.Arguments(0)
   ceUsername = Wscript.Arguments(1)
   cePassword = Wscript.Arguments(2)
   Authorization = Wscript.Arguments(3)
end if

'Load the Crystal Enterprise Session Manager
Dim SessionManager

URL = "http://" & cmsName & "/CmcApp"

Set objIE = CreateObject("InternetExplorer.Application")
objIE.Width = 1900
objIE.Height = 1000
objIE.Left = 0
objIE.Top = 0
objIE.Visible = 1
objIE.Navigate(URL)
wscript.sleep(2000)

GetIE(URL)
Set frames = IE.document.getElementsByTagName("IFrame")

For Each frame In frames

	If frame.name = "CMC_home" Then
		Set getCMCFrame = frame

		Set inputs = getCMCFrame.contentwindow.document.getElementsByTagName("input")

		For Each obj In inputs

			If obj.Name = "cms" Then
				obj.value = cmsName
			End If
			If obj.Name = "username" Then
				obj.value = ceUsername
			End If
			If obj.Name = "password" Then
				obj.value = cePassword
			End If
			If obj.Name = "authType" Then
				obj.value = "Enterprise"
			End If
			if obj.className = "logon_button logon_button_no_hover" then
				wscript.echo "CMC_home = " & obj.className & ", " &  obj.Name
				obj.click

			End if

		Next

	End If
Next

wscript.quit

Sub GetIE(URL)
  Dim objInstances, objIE
  Set objInstances = CreateObject("Shell.Application").windows
  If objInstances.Count > 0 Then '/// make sure we have instances open.
    For Each objIE In objInstances
     If InStr(objIE.LocationURL,URL) > 0 then
       Set IE = objIE
     End if
    Next
  End if
End Sub