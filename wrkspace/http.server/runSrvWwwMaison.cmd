@cls
@chcp 1252
@rem a la maison
@set appHome="C:\CAT_dskD\myTools\Python\wrkspace\www"
@set pyBin="C:\CAT_dskD\myTools\Python\Python36\python.exe"
@set pathRetour="C:\CAT_dskD\myTools\Python\wrkspace"
@set srvAdd=127.0.0.1
@set srvPort=8888
@set srvHome=%apphome%
@rem @set srvBin="C:\CAT_dskD\myTools\Python\wrkspace\http.server\serveurHTTP.py"
@set srvBin=""

cd /D %srvHome%
%pyBin% -m http.server %srvPort% --bind %srvAdd%
cd /D %pathRetour%

chcp 850