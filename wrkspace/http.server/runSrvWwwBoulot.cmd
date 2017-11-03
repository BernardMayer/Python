@rem a la maison
@set appHome="C:\CAT_dskD\myTools\Python\wrkspace\www"
@set pyBin="C:\CAT_dskD\myTools\Python\Python36\python.exe"
@set srvBin="C:\CAT_dskD\myTools\Python\wrkspace\http.server\serveurHTTP.py"
@set srvAdd="--bind 127.0.0.1"
@set srvPort="8888"
@set srvHome=%apphome%

%pyBin% %srvBin% %srvPort% %arvAdd%