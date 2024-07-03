import glob
import os

def find_files(directory, pattern):
    # 디렉토리와 패턴을 결합하여 경로 생성
    search_path = os.path.join(directory, pattern)
    # 패턴에 맞는 모든 파일을 찾음
    files = glob.glob(search_path)
    return files

# 예제 사용법
directory = './log_repo/100011268_10637058_2/Log/ScLogsDatabase'  # 실제 디렉토리 경로로 바꾸세요
pattern = '*KeyBoardShadow*'  # 모든 텍스트 파일을 찾음

found_files = find_files(directory, pattern)

if found_files:
    print(f"Found files: {found_files}")
else:
    print("No files found.")
