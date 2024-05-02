######################################################################################################
# smartsheet 에서 특정 workspace 안의 모든 sheet 정보를 얻어오는 방법
######################################################################################################

# Install the smartsheet sdk with the command: pip install smartsheet-python-sdk
import smartsheet
import logging
import os

_dir = os.path.dirname(os.path.abspath(__file__))


# 특정 column 을 hide 시키는 code
def hide_column_in_sheet(sheet_id):
     # 시트 조회
    sheet = smart.Sheets.get_sheet(sheet_id)

    # 시트의 열 정보 가져오기
    columns = sheet.columns
    for column in columns:
        if column.title == 'Summary':
            update_column = smart.models.Column()
            update_column.hidden = True

            smart.Sheets.update_column(sheet_id, column.id, update_column)
            print("Column Name:", column.title)
            print("Column ID:", column.id)


def create_filter(sheet_id, column_title, target_value):
    # 시트 조회
    sheet = smart.Sheets.get_sheet(sheet_id)

    # 시트의 열 정보 가져오기
    columns = sheet.columns

    # 열 제목을 기반으로 대상 열 찾기
    target_column = None
    for column in columns:
        if column.title == column_title:
            target_column = column
            break

    if target_column is None:
        print("Column with title '{}' not found.".format(column_title))
        return

    # 필터 생성
    new_filter = smart.models.SheetFilter({
        'column_id': target_column.id,
        'criteria': 'CONTAINS',
        'value': target_value
    })


    return new_filter


def apply_filter(sheet_id, new_filter):
    # 필터를 시트에 적용  ==> 함수가 없다고 error 를 만들고 있다.
    response = smart.Sheets.create_filter(
        sheet_id,
        new_filter
    )

    if response.code != 200:
        print("Failed to apply filter. Status code:", response.code)
    else:
        print("Filter applied successfully.")


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

        # print(response)

        # 시트 목록 출력
        # for sheet in response.to_dict()['sheets']:
        #     print("Sheet Name:", sheet['name'])
        #     print("Sheet ID:", sheet['id'])

        # folder 목록 출력
        for folder in response.to_dict()['folders']:
            # print("Folder Name:", folder['name'])
            # print("Folder ID:", folder['id'])

            # If it's the folder you want to retrieve sheets from
            if folder['name'] == "SPR Tracking":  # Change this to the desired folder name
                # Retrieve sheets within the folder
                sheets_in_folder = smart.Folders.get_folder(folder['id'])
                
                # Print sheet details within the folder
                for sheet in sheets_in_folder.sheets:
                    # print("Sheet Name:", sheet.name)
                    # print("Sheet ID:", sheet.id)

                    if sheet.name == "Copy of osprey_issues_FW01":
                        hide_column_in_sheet(sheet.id)

                        # 필터 생성
                        new_filter = create_filter(sheet.id, 'Assigned To', 'dongwoo.lee')

                        # 생성한 필터를 시트에 적용
                        apply_filter(sheet.id, new_filter)
