@cls
@rem @chcp 850
@chcp 1252

@rem @set appHome=D:\myTools\Python\wrkspace\ConnxAll\bin
@set appHome=C:\CAT_dskD\myTools\Python\wrkspace\ConnxAll\bin
@rem @set pyBin=d:\myTools\Python\python36\python.exe
@set pyBin=C:\CAT_dskD\myTools\Python\python36\python.exe

@rem %pyBin% %appHome%\tkinter-HelloWorld.py
@rem %pyBin% %appHome%\tkinter-Menu01.py
@rem %pyBin% %appHome%\tkinter-PanedWindow.py
@rem %pyBin% %appHome%\tkinter-Dispo01.py
@rem %pyBin% %appHome%\tkinter-Dispo02.py
@rem %pyBin% %appHome%\tkinter-Dispo04.py
%pyBin% %appHome%\myApp.py --ini ..\etc\myApp.ini