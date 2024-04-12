######################################################################################################
# smartsheet 에서 특정 workspace 안의 folder 아래에 excel 을 uploading 하여 sheet 를 만드는 sample code 임
######################################################################################################


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


# 워크스페이스 안의 시트 목록 가져오기
workspaces = smart.Workspaces.list_workspaces(include_all=True)

# 작업 공간 및 ID 출력
for workspace in workspaces.data:
    if(workspace.name == "GEUK SW Eng."):
        # Import the sheet
        response = smart.Workspaces.get_workspace(workspace.id)
        print("Workspace Name:", workspace.name)
        print("Workspace ID:", workspace.id)

        # Folder 목록 출력
        for folder in response.to_dict()['folders']:
            print("Folder Name:", folder['name'])
            print("Folder ID:", folder['id'])
            if(folder['name'] == "SPR Tracking"):
                # Import the sheet
                result = smart.Folders.import_xlsx_sheet(folder['id'], _dir+'/Sample Sheet.xlsx', header_row_index=0)

                # Load entire sheet
                sheet = smart.Sheets.get_sheet(result.data.id)

                print("Loaded " + str(len(sheet.rows)) + " rows from sheet: " + sheet.name)
                print("Done")
