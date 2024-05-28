import os

def replace_filename(file_path, new_filename):
    # 파일 경로에서 파일 이름 추출
    old_filename = os.path.basename(file_path)

    # 새로운 파일 경로 생성
    new_file_path = os.path.join(os.path.dirname(file_path), new_filename)

    return  new_file_path
