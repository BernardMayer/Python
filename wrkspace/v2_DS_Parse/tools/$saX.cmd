@cls
@rem @chcp 850
@chcp 1252 >NUL

@set appHome=D:\v2_DSX\tools\bin
@rem @set appHome=C:\CAT_dskD\v2_DSX\tools\bin

@set pyBin=d:\myTools\Python\python36\python.exe
@rem @set pyBin=C:\CAT_dskD\myTools\Python\python36\python.exe

@set dsxHome="D:\v2_DSX\dsx"
@rem @set dsxHome="C:\CAT_dskD\v2_DSX\dsx"

@set fic=Jx_S_DTA_WRK_Enrichissement_PROD_PRODTR_025_1.pjb
@REM Nettoyage du fichier .pjb
@%pyBin% %appHome%\swapBadEntities.py %dsxHome%\%fic% > %dsxHome%\%fic%-clean.txt

@rem @%pyBin% %appHome%\isXshow.py "%dsxHome%\ZUDA0_dsexport_1job.xml"
@%pyBin% %appHome%\xmlDisplayBySax.py "%dsxHome%\%fic%-clean.txt"
