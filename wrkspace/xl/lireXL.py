


import os, sys
import xlrd
##  http://python-simple.com/python-autres-modules-non-standards/xlrd.php
##  https://buildmedia.readthedocs.org/media/pdf/xlrd/latest/xlrd.pdf


sep = "\t"
filenameSrc = "fichierTestLecture.xlsx"
filenameTgt = "fichierResultat.csv"
ligneStart = 2
ligneStop = None
# ligneStop = 3

##  Ouvrir le fichier XL
book = xlrd.open_workbook(filenameSrc)

##  Ouvrir le fichier cible
fdTgt = open(filenameTgt, 'w')
# sheet = book.sheet_by_name('Feuill1')
sheet = book.sheet_by_index(1)
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
  print('Row:', curr_row, sheet.row_values(curr_row))
  fdTgt.write(sep.join(lCells) + "\n")
  if (ligneStop is not None and curr_row >= ligneStop) :
    break
  ##  Ne pas oublier le controle de la boucle :-) 
  curr_row += 1

fdTgt.close()
