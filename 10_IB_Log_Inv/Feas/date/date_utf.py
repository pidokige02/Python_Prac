# from datetime import datetime, timezone, timedelta

# # 주어진 날짜 문자열
# date_str = "2024-04-03 12:39:14.463000 -06:00"

# # 포맷을 지정하여 문자열을 datetime 객체로 변환
# dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f %z")

# # 시간대를 UTC로 변환
# dt_utc = dt.astimezone(timezone.utc)

# print("원래 날짜와 시간:", dt)
# print("UTC로 변환된 날짜와 시간:", dt_utc)


import re
import pandas as pd

def extract_timestamp(timestamp_str):
    try:
        # 정규식을 수정하여 시간대 정보를 포함하도록 함
        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}) ([+-]\d{2}:\d{2})', timestamp_str)
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

# 테스트
timestamp_str = "2024-04-03 12:39:14.463000 -06:00"
result = extract_timestamp(timestamp_str)
print(result)
