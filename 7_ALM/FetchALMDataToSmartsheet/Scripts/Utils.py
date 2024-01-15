from ctypes import windll
import getpass

STD_OUTPUT_HANDLE = -11
reset = 7

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

