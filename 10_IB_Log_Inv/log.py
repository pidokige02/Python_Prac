import re
import pandas as pd
from configure_data import *
from Utils import *


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
            for event, (pattern, isEvent, info_idx) in evant_table_map.items():
                    match = re.search(pattern, row['Text'])
                    if match:
                        event_info = match.group(info_idx) if match.lastindex else match.group(0)
                        self.df.at[index, 'Event'] = event
                        self.df.at[index, 'Info'] = event_info
                        self.df.at[index, 'line#'] = index + 2 # 2 is offset
                        break


    def filter_event(self, event=None):
        if event:
            # 특정 이벤트를 필터링 중복되는 것은 drop 시킴
            self.filtered_df = self.df[self.df['Event'] == event].drop_duplicates(subset='Info')
        else:
            # 'Event' 열이 빈 문자열이 아닌 행만 선택
            self.filtered_df = self.df[(self.df['Event'] != "") & (self.df['Event'] != "S/W version")]

        return self.filtered_df


    def load_device (self, file_path, use_columns_device):
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        try:
            self.df_device = pd.read_csv(file_path, sep='\t', usecols=use_columns_device, encoding='utf-8')
        except UnicodeDecodeError:
            self.df_device = pd.read_csv(file_path, sep='\t', usecols=use_columns_device, encoding='latin1')


    def load_keyevent_log (self, file_path, use_columns_keyevent):
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        try:
            self.df_keyevent = pd.read_csv(file_path, sep='\t', usecols=use_columns_keyevent, encoding='utf-8')
        except UnicodeDecodeError:
            self.df_keyevent = pd.read_csv(file_path, sep='\t', usecols=use_columns_keyevent, encoding='latin1')
        
        self.df_keyevent['Timestamp'] = self.df_keyevent['Timestamp'].apply(extract_timestamp)


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

    def clear_data(self):
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.df_device = pd.DataFrame()
        self.df_keyevent = pd.DataFrame()