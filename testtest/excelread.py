import numpy
import xlrd

excel = xlrd.open_workbook("..//excel//20181-4.xlsx")
all_sheet = excel.sheet_names()
print(all_sheet)
get_sheet = excel.sheet_by_name("平时成绩")

info = []
for i in range(36):
    info_test = []
    for j in range(25):
        info_test.append(get_sheet.cell_value(i, j))
        print(get_sheet.cell_value(i, j), end="\t")
    info.append(info_test)
    print()

print()
for k in info:
    for p in k:
        print(p, end="\t")
    print()


print()
print(info[18][22])


test = numpy.zeros((36, 25))
print(test)


