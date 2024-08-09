from spire.xls import *
from spire.xls.common import *

# list all the files in the directory "storage"
import os
import glob
paths = ["employee-recognition","invoce","payroll"]
save_path = "images"
all_paths = []
for path in paths:
    load_paths = glob.glob(os.path.join("storage",path,"*.xlsx"))
    for table_path in load_paths:
        all_paths.append(table_path)
        # print(table_path)
# print(all_paths)
wb=Workbook()
wb.Worksheets.Clear()
sheet = wb.Worksheets.Add("Style")
sheet.Range["A1"].Text = "File Path"
sheet.Range["B1"].Text = "Color Design"
sheet.Range["C1"].Text = "Font Design"
sheet.Range["D1"].Text = "Border Design"
sheet.Range["E1"].Text = "Alignment Design"
sheet.Range["F1"].Text = "Number Format"
sheet.Range["G1"].Text = "Others"


# store the paths of all the files in the first column of the sheet
for i in range(len(all_paths)):
    sheet.Range["A"+str(i+2)].Text = all_paths[i]

# auto fit the column width
sheet.AllocatedRange.AutoFitColumns()


file_name = "M365StyleAnalysisInit.xlsx"

# delete the file if it exists
if os.path.exists(file_name):
    os.remove(file_name)

wb.SaveToFile(file_name)