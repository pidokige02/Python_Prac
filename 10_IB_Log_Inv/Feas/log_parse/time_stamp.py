import re

# 로그 문자열
log = "1\t1\t2024-03-11 11:08:22.0450000 -06:00\tI\t3160\tScLogsDatabase\tStarting log system\tLogManager.cpp\t125\t42005\t1\tNULL\tNULL\t1"

# 정규 표현식 패턴 정의
# 패턴: 2024-03-11 11:08:22.0450000 -06:00 형식을 찾습니다
timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{7} -\d{2}:\d{2}'

# 정규 표현식을 사용하여 타임스탬프 추출
match = re.search(timestamp_pattern, log)

# 추출한 타임스탬프 저장
if match:
    timestamp = match.group(0)
    print(f"Extracted timestamp: {timestamp}")
else:
    print("No timestamp found in the log.")
