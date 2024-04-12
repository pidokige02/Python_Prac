######################################################################################################
# smartsheet 에서 특정 workspace 안의 모든 sheet 정보를 얻어오는 방법
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
        print("Workspace Name:", workspace.name)
        print("Workspace ID:", workspace.id)
        #get workspace 
        response = smart.Workspaces.get_workspace(workspace.id)

        # 시트 목록 출력
        for sheet in response.to_dict()['sheets']:
            print("Sheet Name:", sheet['name'])
            print("Sheet ID:", sheet['id'])
