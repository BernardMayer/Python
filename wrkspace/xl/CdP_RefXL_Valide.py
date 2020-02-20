


import os, sys, re
import xlrd
##  http://python-simple.com/python-autres-modules-non-standards/xlrd.php
##  https://buildmedia.readthedocs.org/media/pdf/xlrd/latest/xlrd.pdf

##  Ligne1
##  THEME_name	FLUX_NAME	FLUXSET_NAME	INTERFACE_PAGE_CODE	GROUP_NAME	EXTRACTTYPE_NAME	PERIOD_NAME	OBJECT_NAME	FIELD_ORDERBY	FIELD_NAME_TO	FIELD_DESCRIPTION_TO	FIELD_CHARSET_TO	FIELDTYPE_DATASTAGE	FIELD_LENGTH_TO	FIELD_NULLABLE	FIELD_KEY	FIELD_PI	FIELD_TEMPORAL	COMP_MVC	MAPTYPE_NAME	COPY_COBOL	ACQ_DIVIDE_BY_100	ACQ_DEFAULT_4_NULL	FIELD_CHARSET_FROM	FIELDTYPE_DATASTAGE3	FIELD_LENGTH_FROM	FIELD_DEFAULT_FROM	FIELD_FORMAT_FROM	MAPPING_RULE_CODE	MAPPING_VERSION																																				
##  Theme Defaut	DOSS_ENTREES_EN_REL.txt		Windows-1252	EERD_DOSS_ENTREES_EN_REL	COMPLET	J	DOSS_ENTREES_EN_REL	24	DT_NAIS	Date de naissance		Date		Y	N	N			Match	DT_NAIS				Char	10	1900-01-01	DD/MM/YYYY	YYYY-MM-DD	V1																																				


filenameSrc = "2019_CDP_Mapping_OPEN_CHCSIDV2_S50.xlsx"
sheetIndex = 1

THEME_name_cell = 0
THEME_name_values = ()
FLUX_NAME_cell = 1
FLUX_NAME_values = ()
FLUXSET_NAME_cell = 2
FLUXSET_NAME_values = ()
INTERFACE_PAGE_CODE_cell = 3
INTERFACE_PAGE_CODE_values = ('ASCII', 'UTF-8', 'WINDOWS-1252', 'ANSI', 'ISO8859-15')
GROUP_NAME_cell = 4
GROUP_NAME_values = ()
EXTRACTTYPE_NAME_cell = 5
EXTRACTTYPE_NAME_values = ('COMPLET', 'PARTIEL')
PERIOD_NAME_cell = 6
PERIOD_NAME_values = ('D', 'H', 'J', 'M')
OBJECT_NAME_cell = 7
OBJECT_NAME_values = ()
FIELD_ORDERBY_cell = 8
def FIELD_ORDERBY_valid(val) :
    try :
        val = float(val)
        if (val > 0) :
            return True
        else :
            return False
    except ValueError:
        try :
            val = int(val)
            if (val > 0) :
                return True
            else :
                return False
        except ValueError:
            return False
FIELD_NAME_TO_cell = 9
FIELD_NAME_TO_values = ()

sep = "\t"
filenameLog = filenameSrc + ".log"
sheetIndex -= 1
ligneStart = 2
ligneStop = None
# ligneStop = 3

##  Ouvrir le fichier XL
book = xlrd.open_workbook(filenameSrc)

##  Ouvrir le fichier cible
fdLog = open(filenameLog, 'w')
# sheet = book.sheet_by_name('Feuill1')
sheet = book.sheet_by_index(sheetIndex)
# print(sheet.row_values(0))

# sheet.get_rows()

num_rows = sheet.nrows
# curr_row = -1
curr_row = -1 + ligneStart
if (ligneStop is not None) :
    ligneStop -= 1
while curr_row < num_rows:
  row = sheet.row(curr_row)
  lCells = sheet.row_values(curr_row)
  # print('Row:', curr_row, sheet.row_values(curr_row))
  # fdLog.write(sep.join(lCells) + "\n")
  # if (ligneStop is not None and curr_row >= ligneStop) :
    # break
  ##  Les valeurs de la ligne
  INTERFACE_PAGE_CODE = lCells[INTERFACE_PAGE_CODE_cell]
  if (not INTERFACE_PAGE_CODE.upper() in INTERFACE_PAGE_CODE_values) :
    print(str(curr_row) + "___" + str(INTERFACE_PAGE_CODE) + " KO")

  EXTRACTTYPE_NAME = lCells[EXTRACTTYPE_NAME_cell]
  
  FIELD_ORDERBY = lCells[FIELD_ORDERBY_cell]
  if (not FIELD_ORDERBY_valid(FIELD_ORDERBY)) :
    print(str(curr_row) + "___" + str(FIELD_ORDERBY) + " KO\t")
  
  ##  Ne pas oublier le controle de la boucle :-) 
  curr_row += 1

fdLog.close()
