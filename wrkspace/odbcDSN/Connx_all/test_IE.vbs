URL = "http://mup10-itsm.ca-technologies.credit-agricole.fr/arsys/shared/login.jsp?/arsys/forms/mup10-itsmsrgpars/SHR%3ALandingConsole/Default+Administrator+View/?format=html"

Set objIE = CreateObject("InternetExplorer.Application")

wscript.sleep(500)

objIE.Width = 1900
objIE.Height = 1000
objIE.Left = 0
objIE.Top = 0
objIE.Visible = True
wscript.echo "Avant Navigate"
wscript.echo "URL = " & URL
objIE.Navigate URL
wscript.echo  "Apres Navigate"
wscript.quit


