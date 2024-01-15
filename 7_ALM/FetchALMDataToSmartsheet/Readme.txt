##---------------------##
##  How to setup       ##
##---------------------##

1) Need smartsheet licence for using this tool. (If you already have an access token, please skip steps 2-)
2) Open smartsheet, go to Account(left bottom) --> Apps & Integrations --> API Access
3) Click on 'Generate new access token'. Given any name and Click OK
4) Copy the API Access Token(please save it somewhere otherwise you cannot see it again. Need to generate new one)
5) In your PC, set the environment variable SMARTSHEET_ACCESS_TOKEN with the above copied API Access Token
6) Open command prompt as administrator
7) Set proxy with below commands
	>set http_proxy=PITC-Zscaler-Global-ZEN.proxy.corporate.ge.com:80  (replace the proxy if it is different)
	>set https_proxy=PITC-Zscaler-Global-ZEN.proxy.corporate.ge.com:80 (replace the proxy if it is different)
8) Run the below command
	>cd <extracted folder>
	>pip install -r requirements.txt

##---------------------##
##  How to configure   ##
##---------------------##

1) Open Config.INI
2) Configure as per your requirement
3) Password in the config file is optional. If not given, it will prompt to enter password.

##---------------------##
##  How to run         ##
##---------------------##

1) Double click on the AddSPRsToSmartsheet.bat
2) Confirm the there is no errors/warnings(Warnings - Yellow, Errors - Red).


##------------------------------------------------------------------------##
##  Follow below steps create/update user manager mapping in smartsheet   ##
##------------------------------------------------------------------------##

Pre Requisites:
 Create a new smartsheet (one time activity)
 Create new columns Member, Manager with column type Contact List
 Configure the smartsheet id in  'UserDetailsSmartsheetID' field of Config.INI
 Note : 
	If you encounter any error like below while running FindManager.bat	
	''' 
	GetUserDetails.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
    + CategoryInfo          : SecurityError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : UnauthorizedAccess
	'''
	Open PowerShell as administrator and run the below command
		>> "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope LocalMachine"

Open command prompt as administrator and run the bat files in the following order
ExportAlmUsers.bat --> FindManager.bat --> AddUserManagerInfoToSmartSheet.bat

Note: If a prompt is displayed to install AzureAD PowerShell  while running FindManager.bat aknowledge as Yes for all the prompts and Login with GE mail id.