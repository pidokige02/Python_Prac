import os
import re
import pandas as pd
import glob

def replace_filename(file_path, new_filename):
    # 파일 경로에서 파일 이름 추출
    old_filename = os.path.basename(file_path)

    # 새로운 파일 경로 생성
    new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

    return  new_file_path

#타임스탬프 문자열에서 날짜와 시간을 추출하여 pandas의 datetime 형식으로 변환
def extract_timestamp(timestamp_str):
    try:
        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})', timestamp_str)
        if match:
            return pd.to_datetime(match.group(1), format='%Y-%m-%d %H:%M:%S.%f')
        else:
            print(f"Invalid timestamp format: {timestamp_str}")
            return pd.NaT
    except Exception as e:
        print(f"Error parsing timestamp: {timestamp_str}. Error: {e}")
        return pd.NaT

def extract_timestampstring(str):

    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{7}'
    match = re.search(pattern, str)

    if match:
        datetime_info = match.group(0)
        return datetime_info
    else:
        print("Datetime information not found in the text.")

def find_files(directory, pattern):
    # 디렉토리와 패턴을 결합하여 경로 생성
    search_path = os.path.join(directory, pattern)
    # 패턴에 맞는 모든 파일을 찾음
    files = glob.glob(search_path)
    return files

def get_directory_name(file_path):
    return os.path.dirname(file_path)