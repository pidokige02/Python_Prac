import re
import pandas as pd
from configure_data import *
from Util.Utils import *


class Log:
    def __init__(self):
        self.df = None
        self.filtered_df = None

        self.df_device = None
        self.df_keyevent = None


    def load_log (self, file_path, use_columns_log):
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        try:
            self.df = pd.read_csv(file_path, sep='\t', usecols=use_columns_log, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(file_path, sep='\t', usecols=use_columns_log, encoding='latin1')


    # 새로운 열 추가 - 예: 새로운 열 'NewColumn'에 기본값 0 할당
    def add_columns_log (self):

        self.df['Event'] = ""
        self.df['Info'] = ""
        self.df['line#'] = 0
        self.df['keyeventline#'] = 0


    # full log 를 읽어가면서 event 정보 (event nane, event 정보,  원래 full log 의 line#) 을 추가 column 에 표시하는 작업
    def analyze_log (self):
        # 각 이벤트에 대해 정규표현식 적용하여 정보 추출
        for index, row in self.df.iterrows():
            text = row['Text']
            if not isinstance(text, str):
                continue  # 문자열이 아닌 경우 건너뛰기
            for event, (pattern, isEvent, info_idx, skip) in evant_table_map.items():
                    match = re.search(pattern, row['Text'])
                    if match:
                        if(skip != None ):
                            event_info = match.group(info_idx) if match.lastindex else match.group(0)
                            if (event_info !='<none>'):
                                self.df.at[index, 'Event'] = event
                                self.df.at[index, 'Info'] = event_info
                                self.df.at[index, 'line#'] = index + 2 # 2 is offset
                        else:
                            event_info = match.group(info_idx) if match.lastindex else match.group(0)
                            self.df.at[index, 'Event'] = event
                            self.df.at[index, 'Info'] = event_info
                            self.df.at[index, 'line#'] = index + 2 # 2 is offset
                        break


    def filter_event(self, events=None):
        if events:
            if isinstance(events, str):
                events = [events]  # events가 문자열이면 리스트로 변환
            # 특정 이벤트들을 필터링 중복되는 것은 drop 시킴
            self.filtered_df = self.df[self.df['Event'].isin(events)].drop_duplicates(subset='Info')
        else:
            # 'Event' 열이 빈 문자열이 아닌 행만 선택
            self.filtered_df = self.df[(
                self.df['Event'] != "") &
                (self.df['Event'] != "S/W version") &
                (self.df['Event'] != "Product")
                ]

        return self.filtered_df

    def load_device (self, file_path, use_columns_device):
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        try:
            self.df_device = pd.read_csv(file_path, sep='\t', usecols=use_columns_device, encoding='utf-8')
        except UnicodeDecodeError:
            self.df_device = pd.read_csv(file_path, sep='\t', usecols=use_columns_device, encoding='latin1')


    def load_keyevent_log (self, file_paths, use_columns_keyevent):
        dataframes = []
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        for file_path in file_paths:
            try:
                # df = pd.read_csv(file_path, sep='\t', usecols=use_columns_keyevent, encoding='utf-8')
                df = pd.read_csv(file_path, sep='\t',  encoding='utf-8', low_memory=False)    # read the whole field
            except UnicodeDecodeError:
                # df = pd.read_csv(file_path, sep='\t', usecols=use_columns_keyevent, encoding='latin1')
                df = pd.read_csv(file_path, sep='\t', encoding='latin1', low_memory=False)    # read the whole field

            df['Timestamp'] = df['Timestamp'].apply(extract_timestamp)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True)

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


    def analyze_keyevent (self, filtered_df):

        for index, row in filtered_df.iterrows():
            timestamp = row['Timestamp']
            # 가장 가까운 타임스탬프 찾기
            closest_index = (self.df_keyevent['Timestamp'] - extract_timestamp(timestamp)).abs().idxmin()
            filtered_df.at[index, 'keyeventline#'] = self.df_keyevent.at[closest_index, 'keyeventline#']

        return filtered_df

    def clear_eventdata(self):
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()


    def clear_devicedata(self):
        self.df_device = pd.DataFrame()


    def clear_keyeventdata(self):
        self.df_keyevent = pd.DataFrame()


    def locate_keyevent(self, timestamp_str):

        closest_index = (self.df_keyevent['Timestamp'] - extract_timestamp(timestamp_str)).abs().idxmin()
        if closest_index is not None:  # closest_index가 None이 아닌지 확인
            print (f"closest_index is {closest_index} found")
            return closest_index + 2
        else:
            print ("closest_index not found")
            return None