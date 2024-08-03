import datetime

# 현재 날짜와 시간 가져오기
BUILD_TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 타임스탬프를 포함할 파일 경로
timestamp_file = 'build_info.py'

# 타임스탬프를 파일에 기록하기
with open(timestamp_file, 'w') as file:
    file.write(f'BUILD_TIMESTAMP = "{BUILD_TIMESTAMP}"\n')
