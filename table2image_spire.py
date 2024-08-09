from spire.xls import *
from spire.xls.common import *


# list all the files in the directory "storage"
import os
import glob
# paths = ["employee-recognition","invoce","payroll"]
paths = ["employee-recognition"]
save_path = "images"
for path in paths:
    load_paths = glob.glob("storage/"+path+"/*.xlsx")
    for table_path in load_paths[54:]:
        workbook = Workbook()
        print(table_path)
        workbook.LoadFromFile(table_path)
        workbook_name = table_path.split("\\")[-1].split(".")[0]
        # print(workbook_name)
        sheet_id = 0
        for sheet in workbook.Worksheets:
            image = sheet.ToImage(sheet.FirstRow, sheet.FirstColumn , sheet.LastRow, sheet.LastColumn)
            image_path = os.path.join(save_path,path,f"{workbook_name}_{sheet_id}.png")
            if os.path.exists(os.path.join(save_path,path)) == False:
                os.makedirs(os.path.join(save_path,path))
            # print(image_path)
            image.Save(image_path)
            sheet_id += 1
            # break 
        workbook.Dispose()
        # break
    # break
    # print(load_paths)


## test
# workbook = Workbook()
# table_path = "storage/employee-recognition/allowance_tracker.xlsx"
# workbook.LoadFromFile(table_path)
# sheet = workbook.Worksheets.get_Item(0)
# image = sheet.ToImage(sheet.FirstRow, sheet.FirstColumn , sheet.LastRow, sheet.LastColumn)
# image.Save("allowance_tracker.png")
# workbook.Dispose()
# load_paths = ["allowance_tracker.png"]