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
        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6,7}) ([+-]\d{2}:\d{2})', timestamp_str)       
        if match:
            # 시간과 시간대 정보를 모두 포함하여 파싱
            datetime_str = match.group(1) + match.group(2)            
            return pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S.%f%z')
        else:
            print(f"Invalid timestamp format: {timestamp_str}")
            return pd.NaT
    except Exception as e:
        print(f"Error parsing timestamp: {timestamp_str}. Error: {e}")
        return pd.NaT

def extract_timestampstring(timestamp_str):
    # 패턴을 수정하여 시간대 정보를 포함하도록 함
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6,7} [+-]\d{2}:\d{2}'
    match = re.search(pattern, timestamp_str)

    if match:
        datetime_info = match.group(0)
        return datetime_info
    else:
        print("Datetime information not found in the text.")
        return None
    
def find_files(directory, pattern):
    # 디렉토리와 패턴을 결합하여 경로 생성
    search_path = os.path.join(directory, pattern)
    # 패턴에 맞는 모든 파일을 찾음
    files = glob.glob(search_path)
    return files

def get_directory_name(file_path):
    return os.path.dirname(file_path)

def format_timestamp_with_seven_microseconds(timestamp):
    iso_str = timestamp.isoformat()
    # 마이크로초 부분을 추출하여 7자리로 맞춤
    if '.' in iso_str:
        date_part, time_part = iso_str.split('T')
        time_part, offset = time_part.split('-')
        time_part, micro_part = time_part.split('.')
        micro_part = micro_part[:6] + "0"  # 7자리로 맞춤
        formatted_str = f"{date_part} {time_part}.{micro_part} -{offset}"
    else:
        formatted_str = iso_str
    return formatted_str