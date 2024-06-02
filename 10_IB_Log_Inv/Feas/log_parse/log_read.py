import re
import pandas as pd

evant_table_map = {
    'Probe connection' : [r'conn (\d+) name (\S+)'],
    'Probe change' : [r'PRH::SetActiveProbe\(probeId=(\d+)\)'],
    'Application change' : [r'SetApplication\(ES:(\w+)\)'],
    'S/W version' : [r'Overall SW version (\S+)'],
    'Normal shutdown message' : [r'EchoRootPck::PowerOffRack'],
}


# 텍스트 파일 경로
# file_path = '../../log_repo/100011268_10637058_2/Log/ScLogsDatabase/MainLog_1.txt'
file_path = 'MainLog_1.txt'

# 특정 열만 읽기
use_columns = ['Timestamp', 'Text']

# 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
try:
    df = pd.read_csv(file_path, sep='\t', usecols=use_columns, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, sep='\t', usecols=use_columns, encoding='latin1')

# 새로운 열 추가 - 예: 새로운 열 'NewColumn'에 기본값 0 할당
df['Event'] = ""
df['Info'] = ""
df['line#'] = 0


# 각 이벤트에 대해 정규표현식 적용하여 정보 추출
for index, row in df.iterrows():
    text = row['Text']
    if not isinstance(text, str):
        continue  # 문자열이 아닌 경우 건너뛰기    
    for event, patterns in evant_table_map.items():
        for pattern in patterns:
            match = re.search(pattern, row['Text'])
            if match:
                event_info = match.group(1) if match.lastindex else match.group(0)
                df.at[index, 'Event'] = event
                df.at[index, 'Info'] = event_info
                df.at[index, 'line#'] = index + 1
                break


# 'Event' 열이 빈 문자열이 아닌 행만 선택
filtered_df = df[df['Event'] != ""]

# 결과 출력
print(filtered_df)

# 데이터 프레임의 정보를 출력 (데이터 유형, 결측값 등)
print(filtered_df.info())
