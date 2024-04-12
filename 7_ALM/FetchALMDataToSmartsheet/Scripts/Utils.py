from ctypes import windll
import getpass
import os
from datetime import datetime


STD_OUTPUT_HANDLE = -11
reset = 7
configFileName="Config.INI"


def  maximizeCmdWindow():
    windll.user32.ShowWindow( windll.kernel32.GetConsoleWindow(), 3 )

def clearScreen():
    os.system('cls')
    
def printWarning(message):
    color = 14
    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, color)
    print("%s" % (message))
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, reset)

def printError(message):
    color = 12
    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, color)
    print("%s" % (message))
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, reset)
    
def printSuccess(message):
    color = 10
    reset = 7
    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, color)
    print("%s" % (message))
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, reset)

def userInput(message):  
    color = 11
    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, color)
    userData = getpass.getpass(message)
    windll.kernel32.SetConsoleTextAttribute(stdout_handle, reset)
    return str(userData).strip()


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

def get_current_year():
    # 현재 날짜와 시간 얻기
    current_date_time = datetime.now()    
    
    # 현재 날짜만 얻기
    current_year = str(current_date_time.year)

    return current_year

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


def getConfigData():
	global configFileName
	configFile = open(configFileName, "r")
	missingData =[]
	configData ={}
	for eachLine in configFile:
		if eachLine.strip().startswith("#") or eachLine.strip() == "":
			continue
		if "==" in eachLine:
			arrayInfo = eachLine.strip().split("==")
		else:
			arrayInfo = eachLine.strip().split("=")
		if len(arrayInfo)>1 and arrayInfo[1] != "":
			configData[arrayInfo[0].strip()]=arrayInfo[1].strip()
		else:
			if arrayInfo[0] in ['AlmPassword']:
				continue
			missingData.append(arrayInfo[0])
	if(len(missingData)>0):
		printWarning("Below details are missing in {} file \n{}".format(configFileName,str(missingData)))
		return
	return configData


def writeConfigData(configData):  
    global configFileName  # used for test only
    with open(configFileName, "w") as configFile:
        for key, value in configData.items():
            configFile.write(f"{key}={value}\n")
