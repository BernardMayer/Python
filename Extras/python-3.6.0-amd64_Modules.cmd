:: Après avoir installer Python
:: on installe les modules :
:: 	pyodbc (.whl)
:: 	xlrd (.whl)
:: 	xlwt (.whl)
:: 	lxml (.whl)
:: 	geographiclib (.tar.gz)
:: 	gpxpy (.tar.gz)
::	pywin32 et pypiwin32

rem @set home=D:\myTools\Python
@set home=C:\CAT_dskD\myTools\Python
@set pyBin=%home%\Python36\python.exe
@set pipBin=%home%\Python36\Scripts\pip.exe

@echo. 
@echo.INFO :  Install de pyodbc
%pipBin% install %home%\Extras\pyodbc\pyodbc-4.0.11-cp36-cp36m-win_amd64.whl

@echo. 
@echo.INFO :  Install de lxml
%pipBin% install %home%\Extras\lxml\lxml-3.7.3-cp36-cp36m-win_amd64.whl

@echo. 
@echo.INFO :  Install de xlrd
%pipBin% install %home%\Extras\Excel\xlrd-1.0.0-py3-none-any.whl

@echo. 
@echo.INFO :  Install de xlwt
%pipBin% install %home%\Extras\Excel\xlwt-1.2.0-py2.py3-none-any.whl

@echo. 
@rem ! ! ! Faut-il faire avant : pywin32-220.win-amd64-py3.6.exe   ?
@echo.INFO :  Install de pywin32
%pipBin% install %home%\Extras\pywin32\pywin32-220.1-cp36-cp36m-win_amd64.whl

@echo. 
@echo.INFO :  Install de pypiwin32
%pipBin% install %home%\Extras\pywin32\pypiwin32-220-cp36-none-win_amd64.whl

@echo. 
@echo.INFO : Install de geographiclib
cd /d %home%\Extras\geographiclib\geographiclib-1.47
@REM %pyBin% setup.py install
@REM %pyBin% -m unittest geographiclib.test.test_geodesic

@echo. 
@echo.INFO : Install de gpxpy
cd /d %home%\Extras\gpxpy\gpxpy-1.1.2
@REM %pyBin% setup.py install

cd /d %home%