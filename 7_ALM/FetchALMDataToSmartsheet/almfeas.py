import sys
import getpass
import warnings
import os

from  Scripts.AlmRestApi import AlmRestApi
from  Scripts.almtable import *
from  Scripts.export2excel import *
from dotenv import load_dotenv

load_dotenv()

# .env 파일에서 환경변수 로드
almUsername=os.getenv('ALMUSERNAME')
almPassword=os.getenv('ALMPASSWORD')
# -------------------------------------------------------------------

warnings.simplefilter("ignore")

alm = AlmRestApi()

rc = alm.login(almUsername, almPassword)
if rc == 'err_001':
    sys.exit(r'Fail to login')
if rc == 'err_002':
    sys.exit(r'Fail to initialize QC session')

print(r'Logged in succesfully and QC session initialized')

##################################################################
## fetch one defect entity for feasibility testing.
# returndict = alm.get_defects_single()
# print("jinha",returndict)
##################################################################

##################################################################
## fetch the whole defect entities for Osprey R4 Oprey for feasibility testing.
# fields = list(alm_table_map.keys())
# filter = r"{user-01['Osprey R4' or 'Osprey'];id['94173' or '91389' or '94092']}"
# # filter = r"{user-01['Osprey R4' or 'Osprey'];id['94173']}"
# sprs = alm.get_defects_product(filter, fields, 25)
# # print("jinha", sprs)
# spr2excel(sprs,alm_table_header)
##################################################################

# ##################################################################
# ## fetch the whole defect entities for Osprey R4 Oprey for feasibility testing.
# fields = list(alm_table_map.keys())
# filter = r"{user-01['Gemini R5' or 'Gemini R5 Future' or 'Osprey R5' or 'Peregrine R5' or 'Swallow R5']}"
# sprs = alm.get_defects_product(filter, fields, 25)
# spr2excel(sprs,alm_table_header)
# ##################################################################

##################################################################
## fetch the whole defect entities for Osprey R4 Oprey for feasibility testing.
fields = list(alm_table_map.keys())
filter = r"{user-01['Osprey R4' or 'Osprey']}"
# filter = r"{user-01['Gemini R4']}"
sprs = alm.get_defects_product(filter, fields, 25)
spr2excel(sprs,alm_table_header)
##################################################################
alm.logout()


