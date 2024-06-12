######################################################################################################
# 특정 workspace 안의 특정 Folder 아래의 sheet, report, sigtt 정보를 모두 가져오는 sample codes   
# sight id 를 이용하여 sight 안의 widget 를 얻어오는 sample code
######################################################################################################

# Install the smartsheet sdk with the command: pip install smartsheet-python-sdk
import smartsheet
import logging
import os
from datetime import datetime

def get_sight(sight_id):
    try:
        response = smart.Sights.get_sight(sight_id)
        return response
    except Exception as e:
        print(f"Failed to retrieve sight: {e}")
        return None

def parse_date(date_str):
    try:
        # Smartsheet API 날짜 형식 예시: '2024-02-11T22:54:10+00:00Z'
        # 'Z'를 '+00:00'으로 대체하여 파싱
        if date_str.endswith('Z'):
            date_str = date_str[:-1] + '+00:00'
        return datetime.fromisoformat(date_str)
    except Exception as e:
        print(f"Failed to parse date: {e}")
        return None
    
def update_sight(sight_id, sight_obj):
    try:
        response = smart.Sights.update_sight(sight_id, sight_obj)
        print(f"Successfully updated sight {sight_id}")
        return response
    except Exception as e:
        print(f"Failed to update sight: {e}")
        return None

# Sight의 Widget 가져오기
def get_widgets_from_sight(sight_id):
    try:
        response = smart.Sights.get_sight(sight_id)  
        widgets = response.to_dict()["widgets"]
        return widgets
    except Exception as e:
        print(f"Failed to retrieve widgets: {e}")
        return None

   
_dir = os.path.dirname(os.path.abspath(__file__))


print("Starting ...")

# Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
smart = smartsheet.Smartsheet()
# Make sure we don't miss any error
smart.errors_as_exceptions(True)

# Log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

sight_id = 0


# 워크스페이스 안의 시트 목록 가져오기
workspaces = smart.Workspaces.list_workspaces(include_all=True)

# 작업 공간 및 ID 출력
for workspace in workspaces.data:
    if(workspace.name == "GEUK SW Eng."):
        # get workspace 
        response = smart.Workspaces.get_workspace(workspace.id)
        print("Workspace Name:", workspace.name)
        print("Workspace ID:", workspace.id)

        # Folders 목록 출력
        for folder in response.to_dict()['folders']:
            # print("Folder Name:", folder['name'])
            # print("Folder ID:", folder['id'])
            if(folder['name'] == "SW Tasks Tracking and Rollup"):
                response2 = smart.Folders.get_folder(folder['id'])

                # 시트 목록 출력
                for sheet in response2.to_dict()['sheets']:
                    print("Sheet Name:", sheet['name'])
                    print("Sheet ID:", sheet['id'])

                # report 목록 출력
                for report in response2.to_dict()['reports']:
                    print("Report Name:", report['name'])
                    print("Report ID:", report['id'])

                # sight 목록 출력
                for sight in response2.to_dict()['sights']:
                    print("Sight Name:", sight['name'])
                    print("Sight ID:", sight['id'])
                    if(sight['name'] == "Copy of Dashboard - GEUK SW Scrum team"):
                        sight_id = sight['id']

# widget 을 얻어오는 code 로 많은 data 가 넘어온더
# if(sight_id != 0 ):
#     widgets = get_widgets_from_sight(sight_id)
#     if widgets:
#         print("Widgets retrieved successfully:")
#         for widget in widgets:
#             print(widget)

if(sight_id != 0 ):
    widgets = get_widgets_from_sight(sight_id)
    if widgets:
        print("Widgets retrieved successfully:")
        for widget in widgets:
            if 'title' in widget:    # widget 에 'title' key 가 있는지 확인
                print("Widget:", widget)
                if (widget['title'] == 'Osprey R4'):
                    widget_id = widget['id']                
                    shortcuts = widget['contents']['shortcutData']
                    for shortcut in shortcuts:
                        # print("Widget shortcut:", shortcut)
                        if 'hyperlink' in shortcut:    # shortcut 에 'hyperlink' key 가 있는지 확인
                            hyperlink = shortcut['hyperlink']
                            # print("Widget shortcut:", shortcut)
                            if 'sheetId' in hyperlink:    # hyperlink 에 'sheetId' key 가 있는지 확인
                                print("label:", shortcut['label'])
                                # shortcut['label'] = "Test Osprey"
                                # print("label:", shortcut['label'])
                                print("hlink sheetId:", hyperlink['sheetId'])
                                print("hlink url:", hyperlink['url'])
                                # hyperlink['sheetId'] = 8718536511803268
                                print("Updated hlink sheetId:", hyperlink['sheetId'])
                    # print("Widget ID:", widget['id'])
                    # print("Widget Type:", widget['type'])            



# 
# sight = get_sight(sight_id)

# if sight:
#     print("Sight retrieved successfully:")
#     # print("Jinha", sight)
#     sight_dict = sight.to_dict()
#     # print("jinha", sight_dict)
#     # print("jinha", sight_dict['createdAt'])

# # original time string format error 가 뱅생하여 data 만 assign 함
#     sight_dict['createdAt'] = '2024-02-11'
#     # print("jinha1", sight_dict['createdAt'])
#     sight_dict['modifiedAt'] = '2024-02-11'

#     # Modify the sight as needed
#     # For example, update a widget's label
#     for widget in sight_dict.get('widgets', []):
#         if 'title' in widget and widget['title'] == 'Osprey R4':
#             for shortcut in widget.get('contents', {}).get('shortcutData', []):
#                 if 'hyperlink' in shortcut and 'sheetId' in shortcut['hyperlink']:
#                     print("Current label:", shortcut['label'])
#                     shortcut['label'] = "New Label"     # 실제로 바꾸는 code 임
#                     print("Updated label:", shortcut['label'])

#         # erroe 가 발생하여 아래 code 를 추가함
#         # Ensure the 'contents' attribute has the required 'type' key
#         if 'contents' in widget and 'type' not in widget['contents']:
#             widget['contents']['type'] = widget['type']  # Or set a default type if needed

#     # 실제로 위에서 변경한 값이 반영된 것을 확인함
#     print("jinha2", sight_dict)

#     # Convert back to a Sight object
#     # error 없이 updated-sight obkect 가 반환되지만 data 를 잃어버린 상테로 반환이 된다.
#     updated_sight = smartsheet.models.Sight(sight_dict)

#     # print("jinha2", sight_dict) 에서 print 한 것에서 누락이 된 상태가 print 된다. 
#     print("jinha3", updated_sight)

#     # Update the sight
#     update_sight(sight_id, updated_sight)


    