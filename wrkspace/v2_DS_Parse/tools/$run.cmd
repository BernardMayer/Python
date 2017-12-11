@cls >NUL
@rem @chcp 850
@chcp 1252 >NUL

@rem @set appHome=D:\myTools\Python\wrkspace\ConnxAll\bin
@set appHome=C:\CAT_dskD\v2_DSX
@set appHome=D:\v2_DSX\Tools

@rem @set pyBin=d:\myTools\Python\python36\python.exe
@set pyBin=C:\CAT_dskD\myTools\Python\python36\python.exe
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
@rem @%pyBin% %appHome%\bin\DS_GetErrCodeDescription.py --list "%appHome%\var\dsx_20170802.list.txt" --dsxHome "%appHome%\..\dsx"
@rem @%pyBin% -m pdb %appHome%\bin\DS_GetErrCodeDescription.py --list "%appHome%\var\dsx_20170807.list.txt" --dsxHome "%appHome%\..\dsx"
@rem @%pyBin% %appHome%\bin\DS_GetErrCodeDescription.py --list "%appHome%\var\dsx_20170807.list.txt" --dsxHome "%appHome%\..\dsx"
@rem @%pyBin% %appHome%\bin\DS_GetErrCodeDescription.py --list "%appHome%\var\dsx_20170810.list.txt" --dsxHome "%appHome%\..\dsx"
@rem @%pyBin% %appHome%\bin\DS_GetErrCodeDescription.py --list "%appHome%\var\dsx_20170807.list.txt" --dsxHome "%appHome%\..\dsx" --jobObjectVersion "%appHome%\var\MUP10_ObjectsCodeAliasVersion.txt"
@%pyBin% %appHome%\bin\DS_GetErrCodeDescription.py --list "%appHome%\var\dsx_20171024.list.txt" --dsxHome "%appHome%\..\dsx" --jobObjectVersion "%appHome%\var\TargetSourceCodeAliasName_ZUTA0-20171024.txt"