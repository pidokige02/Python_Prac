import os
import re
import pandas as pd

def replace_filename(file_path, new_filename):
    # 파일 경로에서 파일 이름 추출
    old_filename = os.path.basename(file_path)

    # 새로운 파일 경로 생성
    new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

    return  new_file_path

#타임스탬프 문자열에서 날짜와 시간을 추출하여 pandas의 datetime 형식으로 변환
def extract_timestamp(timestamp_str):
    match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})', timestamp_str)
    if match:
        return pd.to_datetime(match.group(1), format='%Y-%m-%d %H:%M:%S.%f')
    else:
        return pd.NaT

