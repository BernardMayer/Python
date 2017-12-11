@cls >NUL
@rem @chcp 850
@chcp 1252 >NUL
@setlocal enabledelayedexpansion

@set appHome=D:\v2_DS_Parse\tools
@set pyBin=d:\myTools\Python\python36\python.exe

@set pyBin=C:\CAT_dskD\myTools\Python\python36\python.exe
@set appHome=C:\RepoGit\Python\wrkspace\v2_DS_Parse\tools

@set parentheseFile="%appHome%\var\Parentheses01.sql"

@%pyBin% %appHome%\bin\parenthese01.py %parentheseFile%
