@cls
@rem @chcp 850
@chcp 1252 >NUL

@rem @set appHome=D:\myTools\Python\wrkspace\ConnxAll\bin
@rem @set appHome=C:\CAT_dskD\v2_DSX\tools\bin
@set appHome=D:\v2_DSX\Tools\bin

@rem @set pyBin=d:\myTools\Python\python36\python.exe
@rem @set pyBin=C:\CAT_dskD\myTools\Python\python36\python.exe
@set pyBin=d:\myTools\Python\python36\python.exe

@rem %pyBin% %appHome%\tkinter-HelloWorld.py
@rem %pyBin% %appHome%\tkinter-Menu01.py
@rem %pyBin% %appHome%\tkinter-PanedWindow.py
@rem %pyBin% %appHome%\tkinter-Dispo01.py
@rem %pyBin% %appHome%\tkinter-Dispo02.py
@rem %pyBin% %appHome%\tkinter-Dispo04.py
@rem @%pyBin% %appHome%\bin\DS_GetErrCodeDescription.py --ini %appHome%\etc\DS_GetErrCodeDescription.ini --list %appHome%\etc\dsx.liste.txt

@REM      Modifier le mtime (attention au .59) touch -m -t 199912312359.59 .\Jx_19991231235959.txt

@REM --dsxHome "c:\ici et la"
@rem @%pyBin% %appHome%\bin\dsXshow.py --list "%appHome%\var\dsx_designer.list.txt" --dsxHome "%appHome%\..\dsx"
@rem @set dsxHome="C:\CAT_dskD\v2_DSX\dsx"
@set dsxHome="D:\v2_DSX\dsx"

@rem @set dsXjobObjectVersionFile=%appHome%\..\var\MUP10_ObjectsCodeAliasVersion.txt
@rem @set dsXjobObjectVersionFile=%appHome%\..\var\MUP10_ObjectsCodeAliasVersionSource-20170824.txt
@rem @set dsXjobObjectVersionFile=%appHome%\..\var\TargetSourceCodeAliasName_ZUTA0-20171024.txt
@set dsXjobObjectVersionFile=%appHome%\..\var\TargetSourceCodeAliasName_MUP10-20171024.txt

@rem @set dsXthisJob=Jx_Sn_DTA_WRK_Enrichissement_ADR_025_1
@rem @set dsXthisJob=Jx_S_DTA_WRK_Enrichissement_A_BDF_MENS_E26_2
@set dsXthisJob=
@set dsXlinenumber=1
@set dsXidentifier=
@set dsXrecordName=
@set dsXstructure=
@set dsXintervar=
@set dsXintervarElse=
@set dsXif=
@set dsXerrcode=
@set dsXerrdescription=
@set dsXshowJobGreater2=
@set dsXshowJobEnrichissement=
@set dsXsynthese=1
@rem @%pyBin% %appHome%\dsXshow.py "%dsxHome%\ZUDA0_designer_0010-qag-20170807.dsx"
@rem @%pyBin% %appHome%\dsXshow.py "%dsxHome%\ZUDA0_dscmdexport-20170807.dsx"
@rem @%pyBin% %appHome%\dsXshow.py "%dsxHome%\ZUTA0_designer_0010-qag-20171024.dsx"
@rem @%pyBin% %appHome%\dsXshow.py "%dsxHome%\MUP10_designer_0010-qag-20171024.dsx" > %appHome%\..\run.log-20171024-MUP10.txt
@%pyBin% %appHome%\dsXshow.py "%dsxHome%\MUP10_designer_DTWH_01-20171024.dsx" > %appHome%\..\run.log-20171024-MUP10-DTWH_01.txt
