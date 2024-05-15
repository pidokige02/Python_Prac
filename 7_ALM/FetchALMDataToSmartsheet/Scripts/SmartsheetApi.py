import smartsheet
from smartsheet import Smartsheet
from smartsheet import sheets

import subprocess
import sys
import logging
from datetime import datetime,timedelta
import time
from .AlmRestApi import AlmRestApi
import warnings
import getpass
from .almtable import *
from .Utils import *
from .smarttable import *
from .export2excel import *
from .xl_utils import *

from dotenv import load_dotenv

load_dotenv()

columnNames={}
deletRowBatch=350
addRowBatch=1000
proxies = {}
smartsheetColumns={}
logger=""
alm = AlmRestApi()
exportUserFileName = "Data\\AlmUserList.txt"
userManagerFileName = "Data\\UserManagerList.txt"

link_file_name = "Data/osprey_link_2024_FW20.xlsx"
report_file_name_osprey_r4 = "Data/osprey_issues_2024_FW20.xlsx"
report_file_name_for_gemini_r3 = "Data/Gemini_R3_issues_2024_FW20.xlsx"	
report_file_name_for_gemini_r4 = "Data/Gemini_R4_issues_2024_FW20.xlsx"
report_file_name_for_gemini_r5 = "Data/Gemini_R5_issues_2024_FW20.xlsx"	

def deleteSheet():
	global smartsheet_client, sheetID

	rows_to_delete = [1, 2, 3]

	delete_result = smartsheet_client.Sheets.delete_rows(sheetID, rows_to_delete)

	# 삭제 결과 확인
	if delete_result:
		print("All rows deleted successfully.")
	else:
		print("Failed to delete rows.")



def exportFromSheet(sheetID):
	global smartsheet_client

	sprs = []
	
	sheet = smartsheet_client.Sheets.get_sheet(sheetID)

	for row in sheet.rows:
		spr = []   # 각 행마다 새로운 빈 리스트를 만듭니다.
		for cell in row.cells:
			spr.append(cell.value)
		sprs.append(spr)

	return sprs 


#  not working w/ message saying not allowed operation
def renameALMColumn(column_id, new_column_title):
	global smartsheet_client, sheetID

    # 열(Column)을 가져오기
	column = smartsheet_client.Sheets.get_column(sheetID, column_id)

    # 새로운 열(Column) 제목 설정
	column.title = new_column_title

    # 변경된 열(Column)을 업데이트   
	response = smartsheet_client.Sheets.update_column(sheetID, column_id, column)

    # 결과 확인
	if response.message == 'SUCCESS':
		print(f'열 이름 변경 성공: 열 ID {column_id}, 새로운 제목: {new_column_title}')
	else:
		print(f'열 이름 변경 중 오류: 열 ID {column_id}, 오류 메시지: {response.message}')



def getAllColumnsProperties(sheetID):
	global smartsheet_client,sheet

	try:
		# 시트 정보 가져오기
		sheet = smartsheet_client.Sheets.get_sheet(sheetID)
		print(f'시트 이름: {sheet.name}')
		print(f'시트 ID: {sheet.id}')

		# first_column = sheet.columns[0]
		# print ("jinha3", first_column)
		# if (first_column.title == "Primary Column"):
		# 	print ("Primary Column is found", first_column.id)
		# 	renameALMColumn(first_column.id, "Project")
		
		for item in sheet.columns:
			print("jinha2", item)

	except smartsheet.exceptions.SmartsheetException as e:
		print(f'시트 정보를 가져오는 중 오류 발생: {e}')



def getColumnsID(columnName):
	global smartsheet_client,sheet,sheetID
	
	# 시트 정보 가져오기
	sheet = smartsheet_client.Sheets

	# 열 목록 조회
	columns = sheet.columns

	# 원하는 열의 이름
	target_column_name = columnName

	for column in columns:
		if column.title == target_column_name:
			target_column_id = column.id
			break
	# 결과 확인
	if target_column_id:
		print(f'열 이름 "{target_column_name}"에 해당하는 열의 ID: {target_column_id}')
		return target_column_id
	else:
		print(f'열 이름 "{target_column_name}"에 해당하는 열을 찾을 수 없습니다.')


def  deleteAllColumns():
	global smartsheet_client,sheet,sheetID

	for column_info in alm_table_map_ss:
	# 열 제거
		response = smartsheet_client.Sheets.delete_column(sheetID, column_info['columnID'])

		# 결과 확인
		if response.message == 'SUCCESS':
			print(f"열 제거 성공: {column_info['columnID']}")
			column_info['columnID'] = 0
		else:
			print(f"열 제거 중 오류: {column_info['columnID']}, 오류 메시지: {response.message}")


def  createALMColumns():
	global smartsheet_client,sheet,sheetID

	# the first column is primary column that should have changed name form "Primary Column" to "Project"
	for column_info in alm_table_map_ss:
	
		column_spec = smartsheet.models.Column({
			'title': column_info['title'],
			'type': column_info['type'],
			'index': column_info['index'],
		})

		response = smartsheet_client.Sheets.add_columns(sheetID, [column_spec])

		# 결과 확인
		if response.message == 'SUCCESS':
			print(f'열 추가 성공: {column_info["title"]}, 열 ID: {response.result[0].id}')
			column_info['columnID'] = response.result[0].id
		else:
			print(f'열 추가 중 오류: {column_info["title"]}, 오류 메시지: {response.message}')




def setProxy(proxy):
	global proxies
	proxies = {
	'https': configData.get(proxy),
	}


def connectToSmartsheet(sheetID):
	try:
		smartsheet_client = smartsheet.Smartsheet()
		smartsheet_client.errors_as_exceptions(True)
		sheet = smartsheet_client.Sheets.get_sheet(sheetID)	
	except Exception as e:   
		print(f"Establishing connection to smartsheet with proxy: {proxies}")
		smartsheet_client=None
	
	try:
		if smartsheet_client is None:
			smartsheet_client = smartsheet.Smartsheet(proxies=proxies)
			smartsheet_client.errors_as_exceptions(True)
			sheet = smartsheet_client.Sheets.get_sheet(sheetID)	
	except Exception as e:
		setProxy("AlternateProxy")
		printWarning(f"Connectoin Failed. Setting 'AlternateProxy':{proxies}")
		smartsheet_client=None
	  
	try:
		if smartsheet_client is None:
			smartsheet_client = smartsheet.Smartsheet(proxies=proxies)
			smartsheet_client.errors_as_exceptions(True)
			sheet = smartsheet_client.Sheets.get_sheet(sheetID)		
		printSuccess("Connection to Smartsheet is Successfull")
		return smartsheet_client,sheet
		
	except Exception as e:
		printException(e,logger)
		printError ("Failed to establish connection to Smartsheet")
		logger.error("Failed to establish connection to Smartsheet")
		return None,None
	
		
# def deleteAllCloumns(columnNamesList):
# 	global sheet
# 	global columnNames
# 	columns = sheet.get_columns(sheetID,include_all=True)
# 	for columnName in columnNamesList:
# 		columnNames[columnName]= {"index":columnNamesList.index(columnName),"newColumn":"Y"}  
# 	print("Finding Unwanted Columns ...")
# 	logger.info("Finding Unwanted Columns ...")
# 	for column in columns.data:
# 		columnId = column.id
# 		if column.title == "Primary Column":
# 			continue
# 		if column.title in columnNames:
# 			columnNames[column.title]["newColumn"]="N"
# 			columnNames[column.title]["id"]=columnId
# 			continue
# 		sheet.delete_column(columnId)
# 		#print("Column Deleted: {}".format(column.title))
# 	print("Unwanted Columns are Deleted\n")
# 	logger.info("Unwanted Columns are Deleted\n")

	
# def addColumns():
# 	newCloumns = []
# 	i=0
# 	for columnName in columnNames:
# 		configDataDet = configData.get(columnName)
# 		if columnName=="Contacts":
# 			column1 = smartsheet.models.Column({
# 				  'title': columnName,
# 				  'type': 'CONTACT_LIST',
# 				  'index': columnNames.get(columnName).get("index")
# 				})
# 		elif configDataDet is not None and len(configDataDet.split("##")) > 1:
# 			columnDet = configDataDet.split("##")
# 			column1 = smartsheet.models.Column({
# 				  'title': columnName,
# 				  'type': columnDet[1] if len(columnDet) > 1 else 'TEXT_NUMBER',
# 				  'index': columnNames.get(columnName).get("index")
# 				})
# 		else:
# 			column1 = smartsheet.models.Column({
# 				  'title': columnName,
# 				  'type': 'TEXT_NUMBER',
# 				  'index': columnNames.get(columnName).get("index")
# 				})
# 		if columnNames.get(columnName).get("newColumn")== "Y":
# 			logger.info("Adding new column columnName:{} Status: {}".format(columnName, columnNames.get(columnName).get("newColumn")))
# 			smartsheet_client.Sheets.add_columns(sheetID,  column1)
# 		else:
# 			logger.info("Updating the column columnName:{} ColumnID: {}".format(columnName, columnNames.get(columnName).get("id")))
# 			smartsheet_client.Sheets.update_column(sheetID, columnNames.get(columnName).get("id"),column1)
# 		i=i+1
		
	
def addUserDetails():
	try:
		rows = []
		response = ""
		r=0
		file = open(userManagerFileName, "r",  encoding='utf-8')
		lines = file.readlines()
		colIdMember = smartsheetColumns.get("Member")
		colIdManager = smartsheetColumns.get("Manager")
		if colIdMember is None:
			printError(f"Column 'Member' not found in the smartsheet '{sheet.name}'")
			sys.exit(0)
		if colIdManager is None:
			printError(f"Column 'Manager' not found in the smartsheet '{sheet.name}'")
			sys.exit(0)
		for eachLine in lines:
			if eachLine.strip() == "":
				continue
			userData = eachLine.split(",")
			if len(userData)<2:
				continue
			user = userData[0]
			manager = userData[1]
			array=smartsheet.models.Row()
			array.to_bottom = True
			array.cells.append({
			'column_id': colIdMember,
			'value': user.strip().lower(),
			'strict': False})
			array.cells.append({
			'column_id': colIdManager,
			'value': manager.strip().lower(),
			'strict': False})
			rows.append(array)
			if len(rows)>addRowBatch:
				r=r+addRowBatch
				response=smartsheet_client.Sheets.add_rows(sheetID, list(rows))
				print("{} rows added".format(r))
				logger.info("{} rows added".format(r))
				rows=[]
		if len(rows)>0:
			r=r+len(rows)
			response=smartsheet_client.Sheets.add_rows(sheetID, list(rows))
			print("{} rows added".format(len(lines)))
			logger.info("{} rows added".format(len(lines)))

	except Exception as e:
		printException(e,logger)
		sys.exit(0)

	
	
def addValues(sprList,userdetails):
	try:
		rows = []
		response = ""
		r=0
		requiredRows = sprList
		prim_column = configData.get("Contacts")
		formulaCoumns = configData.get("Formula_Columns")
		if formulaCoumns is not None:
			formulaCoumns = formulaCoumns.split(",")
		missValFormCol = []
		for row in requiredRows:
			array=smartsheet.models.Row()
			array.to_bottom = True
			for cell in row:
				value = "" if row.get(cell) is None else str(row.get(cell))
				array.cells.append({
					'column_id': smartsheetColumns.get(cell),
					'value': value,
					'strict': False
							})
				if prim_column is not None and cell == prim_column:
					array.cells.append({
					'column_id': smartsheetColumns.get("Contacts"),
					'value': "" if userdetails.get(value) is None else userdetails.get(value),
					'strict': False
							})
			for forCol in formulaCoumns:
				#print(f"{forCol},{smartsheetColumns.get(forCol)}")
				if forCol in missValFormCol:
					continue
				formValue = configData.get(forCol)
				if formValue is None:
					printWarning(f"Value not configured in '{configFileName}' for formula column '{forCol}'")
					missValFormCol.append(forCol)
					continue
				formValue = formValue.split("##")
				formValue = formValue[0]
				array.cells.append({
				'column_id': smartsheetColumns.get(forCol),
				'formula': "" if formValue is None else f"={formValue}",
				'strict': False
						}) 	
				
			rows.append(array)
			if len(rows)>addRowBatch:
				r=r+addRowBatch
				response=smartsheet_client.Sheets.add_rows(sheetID, list(rows))
				print("{} rows added".format(r))
				logger.info("{} rows added".format(r))
				rows=[] 
		if len(rows)>0:
			r=r+len(rows)
			response=smartsheet_client.Sheets.add_rows(sheetID, list(rows))
			print("{} rows added".format(len(sprList)))
			logger.info("{} rows added".format(len(sprList)))

	except Exception as e:
		printException(e,logger)
		sys.exit(0)

def fetchColumnsDetails():
	smartsheetColumns={}
	columns = sheet.get_columns(sheetID,include_all=True)
	#print("Column Details")
	#print("----------------")
	logger.info("Column Details")
	logger.info("----------------")
	
	for column in columns.data:
		#print("{0:40}{1:8}".format(column.title,column.id))
		logger.info("{0:40}{1:8}".format(column.title,column.id))
		smartsheetColumns[column.title]=column.id
	return smartsheetColumns
	#print(smartsheetColumns)

configData = getConfigData()
if configData is None:
	printError("{} file configured incorrectly. Please check".format(configFileName))
	sys.exit()

smartsheet_client,sheet = "",""
sheetID1 = configData.get("SmartsheetID1")
sheetID1 = int(str(sheetID1))

sheetID2 = configData.get("SmartsheetID2")
sheetID2 = int(str(sheetID2))

sheetID3 = configData.get("SmartsheetID3")
sheetID3 = int(str(sheetID3))

sheetID4 = configData.get("SmartsheetID4")
sheetID4 = int(str(sheetID4))

def startLog():
	#logger = logging.getLogger(__name__)  
	logger = logging.getLogger() if configData.get("DetailLog")=="Y" else logging.getLogger(__name__)
	# set log level
	logger.setLevel(logging.WARNING)

	# define file handler and set formatter
	file_handler = logging.FileHandler('logfile.log')
	formatter	= logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
	file_handler.setFormatter(formatter)

	# add file handler to logger
	logger.addHandler(file_handler)
	return logger


	'''
	logger.debug('A debug message')
	logger.info('An info message')
	logger.warning('Something is not right.')
	logger.error('A Major error has happened.')
	logger.critical('Fatal error. Cannot continue')
	'''

def getTimeArray():
	date = datetime.now()
	hoursArray = configData.get("TimeToRefresh").split(",")
	convertedHours = []
	sortedArray =[]
	date = datetime.now()
	for eachHours in hoursArray:
		hrs = eachHours.strip().split(":")
		convertedHours.append(date.replace(hour=int(hrs[0]), minute=int(hrs[1]),second=0,microsecond=0))
	convertedHours.sort()
	sortedArray=convertedHours.copy()
	for eachTime in sortedArray:
		if date >= eachTime:
			convertedHours.remove(eachTime)
			convertedHours.append(eachTime+timedelta(days=1))
	convertedHours.sort()
	#print(convertedHours)
	return convertedHours

def printException(exception,logger):
	#print("Exception: {}".format(type(exception).__name__))
	#print("Exception message: {}".format(exception))
	#print(str(sys.exc_info()))
	print("Error in line {}, {} \n{} \n{}".format(sys.exc_info()[-1].tb_lineno, sys.exc_info()[2].tb_frame.f_code.co_filename, type(exception).__name__, exception))
	logger.error("Error in line {}, {} \n{} \n{}".format(sys.exc_info()[-1].tb_lineno, sys.exc_info()[2].tb_frame.f_code.co_filename, type(exception).__name__, exception))		


def process_Gemini_R4():
	global smartsheet_client,sheet

	##################################################################
	## fetch the whole defect entities for Gemini R4 for feasibility testing.
	fields = list(alm_table_map.keys())
	filter = r"{user-01['Gemini R4' or 'Eagle R4' or 'Eagle R4 Upgrade' or 'Falcon R4' or 'Gemini R4 Dev' or 'Gemini R4 Post Release' or 'Peregrine R4' or 'Swallow R4']}"
	sprs = alm.get_defects_product(filter, fields, 25)
	if (len(sprs)):
		spr2excel(sprs,alm_table_header, alm_table_map)
	else:
		printError("Gemini_R4 ALM data fetch failure")
		return		
	##################################################################

	setProxy("Proxy")
	smartsheet_client,sheet = connectToSmartsheet(sheetID3)
	if smartsheet_client is None:
		printError("Connection to smartsheet failed")
		sys.exit()

	sprs = exportFromSheet(sheetID3)
	sheetspr2excel(sprs, smart_table_header_gemini)

	subprocess.run(["python", "./Scripts/xl_gemi2ospre.py", "./Data/sheetexport.xlsx", "./Data/export.xlsx"])

	report_file_name_for_gemini_r4 = create_product_file("Gemini R4")

	# createdID = excel2sheet(smartsheet_client, configData, report_file_name_for_gemini_r4, "Gemini R4")
	
	# hide_Sheetcolumn(createdID, smart_table_header_gemini)

def process_Gemini_R5():
	global smartsheet_client,sheet

	##################################################################
	## fetch the whole defect entities for Gemini R5 for feasibility testing.
	fields = list(alm_table_map.keys())
	filter = r"{user-01['Gemini R5' or 'Gemini R5 Future' or 'Osprey R5' or 'Peregrine R5' or 'Swallow R5']}"
	sprs = alm.get_defects_product(filter, fields, 25)
	if (len(sprs)):
		spr2excel(sprs,alm_table_header, alm_table_map)
	else:
		printError("Gemini_R5 ALM data fetch failure")
		return		
	##################################################################

	setProxy("Proxy")
	smartsheet_client,sheet = connectToSmartsheet(sheetID2)
	if smartsheet_client is None:
		printError("Connection to smartsheet failed")
		sys.exit()

	sprs = exportFromSheet(sheetID2)
	sheetspr2excel(sprs, smart_table_header_gemini)

	subprocess.run(["python", "./Scripts/xl_smart.py", "./Data/sheetexport.xlsx", "./Data/export.xlsx"])

	report_file_name_for_gemini_r5 = create_product_file("Gemini R5")

	# createdID = excel2sheet(smartsheet_client, configData, report_file_name_for_gemini_r5, "Gemini R5")
	
	# hide_Sheetcolumn(createdID, smart_table_header_gemini)


def process_Gemini_R3():
	global smartsheet_client,sheet

	#################################################################
	## fetch the whole defect entities for Gemini R3 .
	fields = list(alm_table_map.keys())
	filter = r"{user-01['Gemini R3' or 'Eagle R3' or 'Falcon R3' or 'Gemini R3 - Dev' or 'Gemini R3 Future' or 'Gemini R3 Post Release']}"
	sprs = alm.get_defects_product(filter, fields, 25)
	if (len(sprs)):
		spr2excel(sprs,alm_table_header, alm_table_map)
	else:
		printError("Gemini_R3  ALM data fetch failure")
		return		
	##################################################################

	# Smartsheet access
	setProxy("Proxy")
	smartsheet_client,sheet = connectToSmartsheet(sheetID4)
	if smartsheet_client is None:
		printError("Connection to smartsheet failed")
		sys.exit()

	sprs = exportFromSheet(sheetID4)
	sheetspr2excel(sprs, smart_table_header_gemini)

	subprocess.run(["python", "./Scripts/xl_smart.py", "./Data/sheetexport.xlsx", "./Data/export.xlsx"])

	report_file_name_for_gemini_r3 = create_product_file("Gemini R3")

	# createdID = excel2sheet(smartsheet_client, configData, report_file_name_for_gemini_r3, "Gemini R3")
	
	# hide_Sheetcolumn(createdID, smart_table_header_gemini)


def process_Osprey_R4():
	
	global smartsheet_client,sheet
	#################################################################
	## fetch the whole defect entities for Osprey R4 Oprey .
	fields = list(alm_table_map.keys())
	filter = r"{user-01['Osprey R4' or 'Osprey']}"
	sprs = alm.get_defects_product(filter, fields, 25)
	if (len(sprs)):
		spr2excel(sprs,alm_table_header, alm_table_map)
	else:
		printError("Osprey_R4 ALM data fetch failure")
		return		
	##################################################################
	
	# Smartsheet access
	setProxy("Proxy")
	smartsheet_client,sheet = connectToSmartsheet(sheetID1)
	if smartsheet_client is None:
		printError("Connection to smartsheet failed")
		sys.exit()
		
	sprs = exportFromSheet(sheetID1)
	sheetspr2excel(sprs, smart_table_header)

	subprocess.run(["python", "./Scripts/xl_smart.py", "./Data/sheetexport.xlsx", "./Data/export.xlsx"])
	# old data 는 smartsheet 에서 manaul 로 update 한 부분이 있다, new data 는 ALM 에서 capture 한 것으로 최신 status 를 가지고 있다.

	report_file_name_osprey_r4 = create_product_file("Osprey R4")

	#################################################################
	## fetch the link-purpose defect entities for Osprey R4 Oprey.
	fields = list(alm_table_map_for_link.keys())
	filter = r"{user-01['Osprey R4' or 'Osprey']}"
	sprs = alm.get_defects_product(filter, fields, 25)
	if (len(sprs)):
		spr2excel(sprs,alm_link_table_header, alm_table_map_for_link )
	else:
		printError("Osprey_R4_link ALM data fetch failure")
		return		

	##################################################################

	link_file_name = create_product_file("Osprey R4 clone")

	print (link_file_name, report_file_name_osprey_r4, report_file_name_for_gemini_r3, report_file_name_for_gemini_r4, report_file_name_for_gemini_r5)

	# xl_clone_analysis (link_file_name, report_file_name_osprey_r4, report_file_name_for_gemini_r3, report_file_name_for_gemini_r4, report_file_name_for_gemini_r5)

	# createdID = excel2sheet(smartsheet_client, configData, report_file_name_osprey_r4, "Osprey R4")

	# hide_Sheetcolumn(createdID, smart_table_header)

	osprey_issue_path = "./" + report_file_name_osprey_r4

	subprocess.run(["python", "./Scripts/xl_master.py", osprey_issue_path])

	subprocess.run(["python", "./Scripts/xl_analysis.py", "./Data/osprey_issues_master.xlsx"])


def startProcess():
	global smartsheetColumns
	global logger
	datetime1 = datetime.now()
	logger  = startLog()

	for i in range(1, 11):
		process_Gemini_R3()
		process_Gemini_R4()
		process_Gemini_R5()
		process_Osprey_R4()
	return True


def loginToAlm():
	almUsername=os.getenv('ALMUSERNAME')
	almPassword=os.getenv('ALMPASSWORD')

	if almPassword is None:
		almPassword = userInput(r"Enter ALM password: ")

	warnings.simplefilter("ignore")

	rc = alm.login(almUsername, almPassword)
	if rc == 'err_001':
		printError('Failed to login ALM')
		sys.exit()
	if rc == 'err_002':
		printError(r'Failed to initialize ALM session')
		sys.exit()
	printSuccess(r'Logged in succesfully and ALM session initialized')


def hide_Sheetcolumn(sheet_id, arg_smart_table_header):
	print("Hiding unnecessary columns!")
     # 시트 조회
	sheet = smartsheet_client.Sheets.get_sheet(sheet_id)

    # 시트의 열 정보 가져오기
	columns = sheet.columns
	update_column = smartsheet_client.models.Column()

	for column in columns:
		for col, value in arg_smart_table_header.items():
			if column.title == value[0]:
				update_column.hidden = value[1]
				smartsheet_client.Sheets.update_column(sheet_id, column.id, update_column)
				break


	print("Hiding complete!")