# True, faLSE 는 event tracking 을 할지 말지를 정하는 indicator
# 3번째 1, 2 는 원하는  event info 가 있는  
evant_table_map = {
    'S/W version' : [r'Overall SW version (\S+)', False, 1, None],
    'Probe connection' : [r'conn (\d+) name (\S+)', True, 2, None],
    'Probe change' : [r'PRH::SetActiveProbe\(probeId=(\d+)\)',True, 1, None], 
    'Application change' : [r'SetApplication\(ES:(.*?)->',True, 1, None],
    'fatal error' : [r'(fatal)', True, 0, None],
    'shutdown' : [r'(rack power)', True, 0, None],
    'Product' : [r'Initialized for product:\s*(\w+)', False, 1, None],
    'RunState' : [r'RunState\("([^"]+)"\)\s+Modes\("([^"]+)"\)\s+Probe\("([^"]+)"\)\s+Appl\("([^"]+)"\)', True, 2, '<none>']
}




#각 windows 의 dimension
# MAINWIN_DIMENSION="1536x300+0+0"
# LOGWIN_DIMENSION = "968x564+0+350"
# KEYEVENTWIN_DIMENSION = "568x564+968+350"

# raw log file 에서 특정 열만 읽기
use_columns_log = ['Timestamp', 'Text']
# # analysis 후 아래 columne 을 추가하여 필요한 정보를 추가함
# custom_column = ['Event','Info', 'line#']

# raw keyevent file 에서 특정 열만 읽기
use_columns_keyevent = ['Timestamp', 'EventName']


# raw  Devices_1 에서 특정 열만 읽기
use_columns_device = ['Name', 'ProductName', 'MfgName', 'Status']


#event window 에서 보여줄 column 정보
event_columns = [('col1','Timestamp', 50),('col2','Event', 50),('col3','Info', 500),('col4','line#', 15),('col5','keyeventline#', 15)]

peripheral_columns = [('col1','Name', 100),('col2','ProductName', 100),('col3','MfgName',100),('col4','Status',100)]

treeview_index = ("col1", "col2", "col3", "col4", "col5")