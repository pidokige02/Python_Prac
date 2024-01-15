
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.page import PageMargins, PrintOptions
from bs4 import BeautifulSoup 
from openpyxl.utils import get_column_letter

from copy import copy, deepcopy
import sys, os
from datetime import datetime
from .almtable import *


excel_file_name = 'export.xlsx'
template_excel_file_name = 'template.xlsx'


def spr2excel(sprs, alm_table_header):

    report_file_name = excel_file_name

    if os.path.exists(report_file_name):
        print(f"{report_file_name} 파일이 존재합니다.")
        try:
            os.remove(report_file_name)
            print(f"기존 {report_file_name} 파일이 삭제되었습니다.")
        except OSError as e:
            print(f"파일 삭제 실패: {e}")
    
    try:
        column_width_table = {}

        template_wb = load_workbook(template_excel_file_name)
        new_wb = Workbook()

        # #새로운 sheet 생성
        new_sheet = new_wb.active
        template_sheet = template_wb.active

        # get maxcolumn 
        maxcolumn = len(alm_table_header) 

        # append title rowl
        for col, value in alm_table_header.items():
            new_sheet[col+'1'] = value[0]

        # add data ito below row    
        for spr in sprs:
            headers = list(spr.keys())
            sorted_columns = sorted(headers, key=lambda x: list(alm_table_map.keys()).index(x))  # sort it for exported excel
            row_data = [spr[header] for header in sorted_columns]
            new_sheet.append(row_data)

        # get dimension based on template excel file
        for column in template_sheet.iter_cols(min_row=1, max_row=1, min_col=1, max_col=maxcolumn):
            column_letter = column[0].column_letter
            column_width_table[column_letter] = template_sheet.column_dimensions[column_letter].width 

        # set dimension based on template excel file
        for column in new_sheet.iter_cols(min_row=1, max_row=1, min_col=1, max_col=maxcolumn):
            column_letter = column[0].column_letter
            new_sheet.column_dimensions[column_letter].width = column_width_table[column_letter]

        # set html element removed content for DRB session
        for row in new_sheet.iter_rows(min_row=2,min_col=maxcolumn):
            for cell in row:
                html_content = new_sheet[cell.coordinate].value
                soup = BeautifulSoup(html_content, 'html.parser')
                visible_text = soup.get_text(separator=' ', strip=True)
                new_sheet[cell.coordinate].value = visible_text

        # set the property of title
        for row in new_sheet.iter_rows(min_row=1,max_row=1, min_col=1, max_col=maxcolumn):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=False)
                new_sheet[cell.coordinate].fill = copy(template_sheet[cell.coordinate].fill)
                new_sheet[cell.coordinate].font = copy(template_sheet[cell.coordinate].font)
                new_sheet[cell.coordinate].border = copy(template_sheet[cell.coordinate].border)

        # # set the property of spr contents
        for row in new_sheet.iter_rows(min_row=2,min_col=1, max_col=maxcolumn):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=False)
                new_sheet[cell.coordinate].font = copy(template_sheet[get_column_letter(cell.column)+"2"].font)
                new_sheet[cell.coordinate].border = copy(template_sheet[get_column_letter(cell.column)+"2"].border)
                if(cell.row % 2 == 0 ):
                    new_sheet[cell.coordinate].fill = copy(template_sheet[get_column_letter(cell.column)+"2"].fill)
                else:
                    new_sheet[cell.coordinate].fill = copy(template_sheet[get_column_letter(cell.column)+"3"].fill)

        # 열(column) 숨기기
        for column, data in alm_table_header.items():
            new_sheet.column_dimensions[column].hidden = data[2]  # data[2] has hide flag

        # # Save the modified workbook
        new_wb.save(excel_file_name)
        template_wb.save(template_excel_file_name)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except openpyxl.utils.exceptions.InvalidFileException:
        print("올바른 형식의 엑셀 파일이 아닙니다.")
    except Exception as e:
        print("알 수 없는 오류가 발생했습니다:", e)

    finally:
        # Ensure the workbook is closed, even if an exception occurs
        if 'new_wb' in locals():
            new_wb.close()
        if 'template_wb' in locals():
            template_wb.close()


