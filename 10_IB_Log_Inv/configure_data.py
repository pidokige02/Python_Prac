evant_table_map = {
    'S/W version' : [r'Overall SW version (\S+)'],
    'Probe connection' : [r'conn (\d+) name (\S+)'],
    'Probe change' : [r'PRH::SetActiveProbe\(probeId=(\d+)\)'],
    'Application change' : [r'SetApplication\(ES:(\w+)\)'],
    'Normal shutdown message' : [r'EchoRootPck::PowerOffRack'],
}

#각 windows 의 dimension
MAINWIN_DIMENSION="1536x300+0+0"
LOGWIN_DIMENSION = "768x564+0+350"
KEYEVENTWIN_DIMENSION = "768x564+768+350"

# raw log file 에서 특정 열만 읽기
use_columns_log = ['Timestamp', 'Text']
# analysis 후 아래 columne 을 추가하여 필요한 정보를 추가함
custom_column = ['Event','Info', 'line#']


# raw  Devices_1 에서 특정 열만 읽기
use_columns_device = ['Name', 'ProductName', 'MfgName', 'Status']


#event window 에서 보여줄 column 정보
event_columns = [('col1','Timestamp'),('col2','Event'),('col3','Info'),('col4','line#')]

peripheral_columns = [('col1','Name'),('col2','ProductName'),('col3','MfgName'),('col4','Status')]

treeview_index = ("col1", "col2", "col3", "col4")