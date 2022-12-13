import xlwt
import xlrd
from xlutils.copy import copy
import sys

book = xlrd.open_workbook("app/Customer Sales History_2022_11_30.xls")
bookSheet = book.sheet_by_index(0)

newBook = xlwt.Workbook()
newSheet = newBook.add_sheet('Customers')

customersDict = {}
for row in range(0, bookSheet.nrows):
    name = str((bookSheet.cell(row, 0).value))
    if name != "" and name[0].isalpha() and name[0:7]!="Invoice" and name[0:5]!="Guest":
        purchases = []
        startRow = row + 2
        col = 2

        emptyCount = 0
        for purchaseRow in range(startRow, sys.maxsize):
            if purchaseRow == bookSheet.nrows:
                break

            if emptyCount == 2:
                break

            purchase = bookSheet.cell(purchaseRow, col).value
            if purchase == "":
                emptyCount+=1
                pass
            else:
                purchases.append(purchase)
                emptyCount = 0
        
        customersDict.update({name: purchases})

print(customersDict)
# print(customersDict.keys())

#newBook.save("newBook.xls")