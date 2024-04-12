###############################################################################################################
# smartsheet 에서 특정 workspace 아래에 excel 을 uploading 하여 sheet 를 만들고 sheetID를 이용하여 sheet delete 함
##############################################################################################################


# Install the smartsheet sdk with the command: pip install smartsheet-python-sdk
import smartsheet
import logging
import os

_dir = os.path.dirname(os.path.abspath(__file__))


print("Starting ...")

# Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
smart = smartsheet.Smartsheet()
# Make sure we don't miss any error
smart.errors_as_exceptions(True)

# Log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)


# 작업 공간 목록 가져 오기
workspaces = smart.Workspaces.list_workspaces(include_all=True)

# 작업 공간 및 ID 출력
for workspace in workspaces.data:
    if(workspace.name == "GEUK SW Eng."):
        # Import the sheet
        result = smart.Workspaces.import_xlsx_sheet(workspace.id, _dir+'/Sample Sheet.xlsx', header_row_index=0)
        print("Workspace Name:", workspace.name)
        print("Workspace ID:", workspace.id)

# Load entire sheet
if (result.data.id):
    sheet = smart.Sheets.get_sheet(result.data.id)
    print("Loaded " + str(len(sheet.rows)) + " rows from sheet: " + sheet.name, "with " + str(sheet.id))
    smart.Sheets.delete_sheet(sheet.id)

    print("Deleting!!" + str(sheet.id) + " Done")
