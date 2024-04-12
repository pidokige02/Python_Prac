import smartsheet

# Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
smart = smartsheet.Smartsheet()


# 작업 공간 목록 가져 오기
workspaces = smart.Workspaces.list_workspaces(include_all=True)

# 작업 공간 및 ID 출력
for workspace in workspaces.data:
    if(workspace.name == "GEUK SW Eng."):
        print("Workspace Name:", workspace.name)
        print("Workspace ID:", workspace.id)

