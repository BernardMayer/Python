@cls >NUL
@rem @chcp 850
@chcp 1252 >NUL
@setlocal enabledelayedexpansion

@rem @set appHome=D:\v2_DS_Parse\tools
@rem @set pyBin=d:\myTools\Python\python36\python.exe

@set appHome=C:\RepoGit\Python\wrkspace\v2_DS_Parse\tools
@set pyBin=C:\CAT_dskD\myTools\Python\python36\python.exe


@set isxFile="%appHome%\..\jobs\Jx_S_DTA_WRK_Enrichissement_PROD_PRODTR_025_1.pjb.20171205"
@rem @set isxFile="%appHome%\..\jobs\Jx_S_DTA_WRK_Enrichissement_PROD_PRODTR_025_1.pjb.20170825"

@%pyBin% %appHome%\bin\isxParse.py %isxFile%
