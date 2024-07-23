import re
import pandas as pd
from configure_data import *
from Util.Utils import *


class Log:
    def __init__(self):
        self.df_mainlog = None
        self.df_filtered = None

        self.df_device = None
        self.df_keyevent = None
        
        # crash data의 첫번째 line 만 읽어서 표시하기 위하여 
        self.first_lines_with_timestamps = {}



    def load_log (self, file_paths, use_columns_log):
        dataframes = []
        target_tz = None
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path, sep='\t', usecols=use_columns_log, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, sep='\t', usecols=use_columns_log, encoding='latin1')

            # Apply extract_timestamp only to non-null values
            df['Timestamp'] = df['Timestamp'].apply(
                lambda x: extract_timestamp(x) if pd.notnull(x) else x
            )

            # Remove rows with invalid or unnecessary content, such as "(200000 rows affected)"
            df = df[pd.notnull(df['Timestamp'])]

            # Get the timezone of the first valid timestamp if not already set
            if target_tz is None:
                first_valid_timestamp = df['Timestamp'].dropna().iloc[0]
                target_tz = first_valid_timestamp.tz
            # Convert all timestamps to the target timezone
            df['Timestamp'] = df['Timestamp'].apply(lambda x: x.astimezone(target_tz) if pd.notnull(x) else x)

            dataframes.append(df)

        # Concatenate all dataframes
        if dataframes:
            self.df_mainlog = pd.concat(dataframes, ignore_index=True)
        else:
            self.df_mainlog = pd.DataFrame(columns=use_columns_log)


    # 새로운 열 추가 - 예: 새로운 열 'NewColumn'에 기본값 0 할당
    def add_columns_log (self):

        self.df_mainlog['Event'] = ""
        self.df_mainlog['Info'] = ""
        self.df_mainlog['line#'] = 0
        self.df_mainlog['keyeventline#'] = 0


    # full log 를 읽어가면서 event 정보 (event nane, event 정보,  원래 full log 의 line#) 을 추가 column 에 표시하는 작업
    def analyze_log (self):
        # 각 이벤트에 대해 정규표현식 적용하여 정보 추출
        for index, row in self.df_mainlog.iterrows():
            text = row['Text']
            if not isinstance(text, str):
                continue  # 문자열이 아닌 경우 건너뛰기
            for event, (pattern, isEvent, info_idx, skip) in evant_table_map.items():
                    match = re.search(pattern, row['Text'])
                    if match:
                        if(skip != None ):
                            if event == 'RunState':
                                # 'RunState' 이벤트의 경우 여러 그룹을 결합하여 event_info를 구성
                                event_info = f"{match.group(1)} / {match.group(2)} / {match.group(3)}"
                            else:
                                event_info = match.group(info_idx) if match.lastindex else match.group(0)
                            if (event_info !='<none>'):
                                self.df_mainlog.at[index, 'Event'] = event
                                self.df_mainlog.at[index, 'Info'] = event_info
                                self.df_mainlog.at[index, 'line#'] = index + 2 # 2 is offset
                        else:
                            event_info = match.group(info_idx) if match.lastindex else match.group(0)
                            self.df_mainlog.at[index, 'Event'] = event
                            self.df_mainlog.at[index, 'Info'] = event_info
                            self.df_mainlog.at[index, 'line#'] = index + 2 # 2 is offset
                        break


    def filter_event(self, events=None):
        if events:
            if isinstance(events, str):
                events = [events]  # events가 문자열이면 리스트로 변환
            # 특정 이벤트들을 필터링 중복되는 것은 drop 시킴
            self.df_filtered = self.df_mainlog[self.df_mainlog['Event'].isin(events)].drop_duplicates(subset='Info')
        else:
            # 'Event' 열이 빈 문자열이 아닌 행만 선택
            self.df_filtered = self.df_mainlog[(
                self.df_mainlog['Event'] != "") &
                (self.df_mainlog['Event'] != "S/W version") &
                (self.df_mainlog['Event'] != "Product")
                ]

        return self.df_filtered

    def load_device (self, file_path, use_columns_device):
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        try:
            self.df_device = pd.read_csv(file_path, sep='\t', usecols=use_columns_device, encoding='utf-8')
        except UnicodeDecodeError:
            self.df_device = pd.read_csv(file_path, sep='\t', usecols=use_columns_device, encoding='latin1')


    def load_keyevent_log (self, file_paths, use_columns_keyevent):
        dataframes = []
        target_tz = None

        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path, sep='\t', usecols=use_columns_keyevent, encoding='utf-8')
                # df = pd.read_csv(file_path, sep='\t',  encoding='utf-8', low_memory=False)    # read the whole field
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, sep='\t', usecols=use_columns_keyevent, encoding='latin1')
                # df = pd.read_csv(file_path, sep='\t', encoding='latin1', low_memory=False)    # read the whole field

            df['Timestamp'] = df['Timestamp'].apply(extract_timestamp)

            # Remove rows with invalid or unnecessary content, such as "(200000 rows affected)"
            df = df[pd.notnull(df['Timestamp'])]

            # Get the timezone of the first valid timestamp if not already set
            if target_tz is None:
                first_valid_timestamp = df['Timestamp'].dropna().iloc[0]
                target_tz = first_valid_timestamp.tz

            # Convert all timestamps to the target timezone
            df['Timestamp'] = df['Timestamp'].apply(lambda x: x.astimezone(target_tz) if pd.notnull(x) else x)

            dataframes.append(df)

        # Concatenate all dataframes
        if dataframes:
            self.df_keyevent = pd.concat(dataframes, ignore_index=True)
        else:
            self.df_keyevent = pd.DataFrame(columns=use_columns_keyevent)


    def add_columns_keyevent (self):
        self.df_keyevent['keyeventline#'] = 0

        #line# 를 미리 넣어 둔다.
        for index, row in self.df_keyevent.iterrows():
            timestamp = row['Timestamp']
            if pd.isna(timestamp):
                continue  # 유효하지 않은 타임스탬프는 건너뛰기
            self.df_keyevent.at[index, 'keyeventline#'] = index + 2


    def analyze_keyevent (self, df_filtered):

        for index, row in df_filtered.iterrows():
            timestamp = row['Timestamp']
            # 가장 가까운 타임스탬프 찾기
            closest_index = (self.df_keyevent['Timestamp'] - timestamp).abs().idxmin()
            df_filtered.at[index, 'keyeventline#'] = self.df_keyevent.at[closest_index, 'keyeventline#']

        return df_filtered

    def clear_eventdata(self):
        self.df_mainlog = pd.DataFrame()
        self.df_filtered = pd.DataFrame()


    def clear_devicedata(self):
        self.df_device = pd.DataFrame()


    def clear_keyeventdata(self):
        self.df_keyevent = pd.DataFrame()


    def clear_crashdata(self):
        self.first_lines_with_timestamps = {}    


    def locate_keyevent(self, timestamp_str):
        if '.' in timestamp_str and '+' in timestamp_str:  # 2024-05-03 15:21:45.0460000 +05:30
            timestamp = extract_timestamp(timestamp_str)
        else:
            timestamp = extract_simpler_timestamp(timestamp_str)  # 2024-05-03 15:21:45
            # Assuming the dataframe timestamps are tz-aware, make the extracted timestamp tz-aware
            if not self.df_keyevent['Timestamp'].dt.tz is None:
                timezone = self.df_keyevent['Timestamp'].dt.tz
                # Use replace to add timezone information
                timestamp = timestamp.replace(tzinfo=timezone)
            else:
                # Handle the case where the dataframe timestamps are not tz-aware
                # This should ideally not happen if the data is consistent
                pass

        closest_index = (self.df_keyevent['Timestamp'] - timestamp).abs().idxmin()
        if closest_index is not None:  # closest_index가 None이 아닌지 확인
            print (f"closest_index is {closest_index} found")
            return closest_index + 2
        else:
            print ("closest_index not found")
            return None
        
    
    def load_crashdata(self, file_paths, timestamps):
        for file_path, timestamp in zip(file_paths, timestamps):
            try:
                with open(file_path, 'r') as file:
                    first_line = file.readline().strip()
                    self.first_lines_with_timestamps[(file_path, timestamp)] = first_line
                    # file_path 와 timestamp 를 index 로 하여 first line 정보를 저장함
            except Exception as e:
                self.first_lines_with_timestamps[(file_path, timestamp)] = f"Error: {e}"


    def locate_logeventt(self, timestamp_str):
        if '.' in timestamp_str and '+' in timestamp_str:  # 2024-05-03 15:21:45.0460000 +05:30
            timestamp = extract_timestamp(timestamp_str)
        else:
            timestamp = extract_simpler_timestamp(timestamp_str)  # 2024-05-03 15:21:45
            # Assuming the dataframe timestamps are tz-aware, make the extracted timestamp tz-aware
            if not self.df_mainlog['Timestamp'].dt.tz is None:
                timezone = self.df_mainlog['Timestamp'].dt.tz
                # Use replace to add timezone information
                timestamp = timestamp.replace(tzinfo=timezone)
            else:
                # Handle the case where the dataframe timestamps are not tz-aware
                # This should ideally not happen if the data is consistent
                pass

        closest_index = (self.df_mainlog['Timestamp'] - timestamp).abs().idxmin()
        if closest_index is not None:  # closest_index가 None이 아닌지 확인
            print (f"closest_index is {closest_index} found")
            return closest_index + 2
        else:
            print ("closest_index not found")
            return None