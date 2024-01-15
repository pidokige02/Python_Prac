import smartsheet
from smartsheet import Smartsheet
from smartsheet import sheets
import sys
import logging
from datetime import datetime,timedelta
import time
from .AlmRestApi import AlmRestApi
import warnings
import getpass
from .Utils import *

configFileName="Config.INI"
columnNames={}
deletRowBatch=350
addRowBatch=1000
proxies = {}
smartsheetColumns={}
logger=""
alm = AlmRestApi()
exportUserFileName = "Data\\AlmUserList.txt"
userManagerFileName = "Data\\UserManagerList.txt"

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
	
		
def deleteAllCloumns(columnNamesList):
	global sheet
	global columnNames
	columns = sheet.get_columns(sheetID,include_all=True)
	for columnName in columnNamesList:
		columnNames[columnName]= {"index":columnNamesList.index(columnName),"newColumn":"Y"}  
	print("Finding Unwanted Columns ...")
	logger.info("Finding Unwanted Columns ...")
	for column in columns.data:
		columnId = column.id
		if column.title == "Primary Column":
			continue
		if column.title in columnNames:
			columnNames[column.title]["newColumn"]="N"
			columnNames[column.title]["id"]=columnId
			continue
		sheet.delete_column(columnId)
		#print("Column Deleted: {}".format(column.title))
	print("Unwanted Columns are Deleted\n")
	logger.info("Unwanted Columns are Deleted\n")

	
def addColumns():
	newCloumns = []
	i=0
	for columnName in columnNames:
		configDataDet = configData.get(columnName)
		if columnName=="Contacts":
			column1 = smartsheet.models.Column({
				  'title': columnName,
				  'type': 'CONTACT_LIST',
				  'index': columnNames.get(columnName).get("index")
				})
		elif configDataDet is not None and len(configDataDet.split("##")) > 1:
			columnDet = configDataDet.split("##")
			column1 = smartsheet.models.Column({
				  'title': columnName,
				  'type': columnDet[1] if len(columnDet) > 1 else 'TEXT_NUMBER',
				  'index': columnNames.get(columnName).get("index")
				})
		else:
			column1 = smartsheet.models.Column({
				  'title': columnName,
				  'type': 'TEXT_NUMBER',
				  'index': columnNames.get(columnName).get("index")
				})
		if columnNames.get(columnName).get("newColumn")== "Y":
			logger.info("Adding new column columnName:{} Status: {}".format(columnName, columnNames.get(columnName).get("newColumn")))
			smartsheet_client.Sheets.add_columns(sheetID,  column1)
		else:
			logger.info("Updating the column columnName:{} ColumnID: {}".format(columnName, columnNames.get(columnName).get("id")))
			smartsheet_client.Sheets.update_column(sheetID, columnNames.get(columnName).get("id"),column1)
		i=i+1
		
	
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

def deleteAllRows():
	print("Deleting all rows from smartsheet")
	logger.info("Deleting all rows ...")
	all_rows=smartsheet_client.Sheets.get_sheet(sheetID)
	rowsArray =[]
	for row in list(all_rows.rows):
		rowsArray.append(row.id)
		if (len(rowsArray)>deletRowBatch):
			smartsheet_client.Sheets.delete_rows(sheetID,rowsArray)
			rowsArray=[]
	if len(rowsArray)>0 :
		smartsheet_client.Sheets.delete_rows(sheetID,rowsArray)
	print("All Rows Deleted\n")
	logger.info("All Rows Deleted")
	
		

configData = getConfigData()
if configData is None:
	 printError("{} file configured incorrectly. Please check".format(configFileName))
	 sys.exit()

smartsheet_client,sheet = "",""
sheetID = configData.get("SmartsheetID")
sheetID = int(str(sheetID))

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

def startProcess():
	global smartsheetColumns
	global logger
	global smartsheet_client,sheet
	datetime1 = datetime.now()
	logger  = startLog()

	# # jinha comment out until smartsheet access is available	
	# # Alm operations
	# filterName = configData.get("FilterName")
	# formulaCoumns = configData.get("Formula_Columns")
	# if formulaCoumns is not None:
	# 	formulaCoumns = formulaCoumns.split(",")
	# sprList = alm.get_defects_by_filter_name(filterName)
	# if sprList is None:
	# 	printWarning("SPR list is empty. Data not added to smartsheet")
	# 	sys.exit()
	# filter_id=alm.get_favorite_filter_id(filterName)
	# reqColumns = alm.fav_filter_columns_actual_name(filter_id)
	# reqColumns.append("Contacts")
	# [reqColumns.append(forCol) for forCol in formulaCoumns]
	# userDetails = alm.get_user_details()
	# print("Total SPR(s) Count: {}".format(len(sprList)))
	
	# Smartsheet operations
	setProxy("Proxy")
	print ('jinha sheetID',sheetID)
	smartsheet_client,sheet = connectToSmartsheet(sheetID)
	if smartsheet_client is None:
		printError("Connection to smartsheet failed")
		sys.exit()
	deleteAllCloumns(reqColumns)
	deleteAllRows()
	addColumns()
	smartsheetColumns = fetchColumnsDetails()
	addValues(sprList,userDetails)
	datetime2 = datetime.now()
	difference = datetime2.replace(microsecond=0) - datetime1.replace(microsecond=0)
	
	printSuccess(f"\nAll rows are added to smartsheet '{sheet.name}'\nUrl : {sheet.permalink}")
	logger.info(f"All rows are added to smartsheet '{sheet.name}'\nUrl : {sheet.permalink}")
	print("Total time taken: {}".format(difference))
	logger.info("Total time taken: {}".format(difference))
	return True


def exportUserDetails():
	userDetails = alm.get_user_details()
	with open(exportUserFileName, "w") as file:
		file.writelines(userDetails.get(u) + '\n' for u in userDetails)
	printSuccess(f'Alm User details exported to file {exportUserFileName}')

def addUserToSmartsheet():
	global smartsheetColumns
	global logger
	global smartsheet_client,sheet,sheetID
	sheetID = configData.get("UserDetailsSmartsheetID")
	logger  = startLog()
	setProxy("Proxy")
	smartsheet_client,sheet = connectToSmartsheet(sheetID)
	if smartsheet_client is None:
		printError("Connection to smartsheet failed")
		sys.exit()
	deleteAllRows()
	smartsheetColumns = fetchColumnsDetails()
	addUserDetails()
	printSuccess(f"User and Manager mapping added to smartsheet '{sheet.name}' \nUrl : {sheet.permalink}")
	
'''
def main(stopped):
	processStatus = startProcess()
	timeArray= getTimeArray()
	if not processStatus:
		print("Next retry is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
		logger.info("Next retry is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
	else:
		print("Next update is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
		logger.info("Next update is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
	while(not stopped):
		if(datetime.now() > timeArray[0]):
			processStatus = startProcess()
			timeArray.append(timeArray[0]+timedelta(days=1))
			timeArray.pop(0)
			if not processStatus:
				print("Next retry is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
				logger.info("Next retry is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
			else:
				print("Next update is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
				logger.info("Next update is scheduled at {}".format(timeArray[0].strftime("%d-%m-%Y %H:%M:%S")))
			
'''
def loginToAlm():
	# almUsername = configData.get("AlmUserName")
	# almPassword = configData.get("AlmPassword")
	almUsername="jin ha.hwang"
	almPassword="oct1006minja"

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


# value '2' for export user list
# value '2' for add user list to smartsheet
###############################################
# commented by jinha for feasibility test 
# args = 1
# if len(sys.argv) > 1:
# 	args = sys.argv[1]
# 	if args == "2":
# 		loginToAlm()
# 		exportUserDetails()
# 	elif args == "3":
# 		addUserToSmartsheet()
# else:
# 	loginToAlm()
# 	startProcess()