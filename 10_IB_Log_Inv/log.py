import re
import pandas as pd
from configure_data import *


class Log:
    def __init__(self):
        self.df = None
        self.filtered_df = None 

        self.df_device = None


    def load_log (self, file_path, use_columns_log):
        # 탭으로 구분된 텍스트 파일을 인코딩을 지정하여 데이터 프레임으로 읽기
        try:
            self.df = pd.read_csv(file_path, sep='\t', usecols=use_columns_log, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(file_path, sep='\t', usecols=use_columns_log, encoding='latin1')

    # 새로운 열 추가 - 예: 새로운 열 'NewColumn'에 기본값 0 할당
    def add_columns (self):

        self.df['Event'] = ""
        self.df['Info'] = ""
        self.df['line#'] = 0

    # full log 를 읽어가면서 event 정보 (event nane, event 정보,  원래 full log 의 line#) 을 추가 column 에 표시하는 작업
    def analyze_log (self):
        # 각 이벤트에 대해 정규표현식 적용하여 정보 추출
        for index, row in self.df.iterrows():
            text = row['Text']
            if not isinstance(text, str):
                continue  # 문자열이 아닌 경우 건너뛰기    
            for event, patterns in evant_table_map.items():
                for pattern in patterns:
                    match = re.search(pattern, row['Text'])
                    if match:
                        event_info = match.group(1) if match.lastindex else match.group(0)
                        self.df.at[index, 'Event'] = event
                        self.df.at[index, 'Info'] = event_info
                        self.df.at[index, 'line#'] = index + 1
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

