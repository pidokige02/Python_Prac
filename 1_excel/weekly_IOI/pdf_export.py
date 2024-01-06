import win32com.client
import os
from datetime import datetime


def file_name_change(oldfilename, new_filename):
    if os.path.exists(new_filename):
        print(f"기존 {new_filename} 파일이 존재합니다.")
        try:
            os.remove(new_filename)
            print(f"기존 {new_filename} 파일이 삭제되었습니다.")
        except OSError as e:
            print(f"파일 삭제 실패: {e}")
    
    os.rename(oldfilename, new_filename)

def get_current_date():
    # 현재 날짜와 시간 얻기
    current_date_time = datetime.now()    
    
    # 현재 날짜만 얻기
    current_date = current_date_time.date()

    return current_date


def date_to_fw_format(input_date):
    # 입력된 날짜를 파싱
    date_object = datetime.strptime(str(input_date), '%Y-%m-%d')

    # 날짜에서 년도와 주차(WW) 추출
    year = date_object.year
    week_number = date_object.strftime('%U')
    week_number = int(week_number)+1 # start FW01 not FW00 
    str_week_number = str(week_number)

    # FWxx 형식으로 포맷팅
    fw_format = f'FW{str_week_number.zfill(2)}'

    return fw_format
       
def get_absolate_path (filepath):
    absolute_path = os.path.abspath(filepath)

    # print(f"절대 경로: {absolute_path}")
    return absolute_path


def excel_to_pdf(excel_file, pdf_file, sheet_name):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    # Excel 파일 열기
    workbook = excel.Workbooks.Open(excel_file)
    
    try:
        # 원하는 시트 선택
        worksheet = workbook.Sheets(sheet_name)

        # PDF로 인쇄
        worksheet.ExportAsFixedFormat(0, pdf_file)
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        # Excel 종료
        workbook.Close(False)
        excel.Quit()

excel_file_path = r'C:\Users\305005679\Documents\GitHub\Python_Prac\1_excel\weekly_IOI\copied.xlsx'  # Replace with the actual Excel file path
pdf_file_path = r'C:\Users\305005679\Documents\GitHub\Python_Prac\1_excel\weekly_IOI\copied.pdf'      # Specify the desired PDF file path
excel_file = 'copied.xlsx'  
pdf_file = 'copied.pdf'      

sheet_name = 'Sheet'             # Replace with the desired sheet name

excel_file_path = get_absolate_path(excel_file)
pdf_file_path = get_absolate_path(pdf_file_path)

excel_to_pdf(excel_file_path, pdf_file_path, sheet_name)

today = get_current_date()
fw_format = date_to_fw_format (today)

new_file_name = f"{fw_format}_IOI_GI_SW_Engineering.xlsx"
file_name_change(excel_file, new_file_name)

new_file_name = f"{fw_format}_IOI_GI_SW_Engineering.pdf"
file_name_change(pdf_file_path, new_file_name)


