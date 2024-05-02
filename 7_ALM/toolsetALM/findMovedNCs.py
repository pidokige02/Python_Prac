import sys
import getpass
import warnings
import os

from AlmRestApi import AlmRestApi
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# make following as a user input:
# almUsername = input(r"Enter ALM username: ")
# almPassword =  getpass.getpass(r"Enter ALM password: ")
almUsername=os.getenv('ALMUSERNAME')
almPassword=os.getenv('ALMPASSWORD')
# almBgn = input(r"Enter first date of the period date (yyyy-mm-dd): ")
# almEnd = input(r"Enter date of next day after the period (yyyy-mm-dd): ")

# -------------------------------------------------------------------

warnings.simplefilter("ignore")

alm = AlmRestApi()

rc = alm.login(almUsername, almPassword)
if rc == 'err_001':
    sys.exit(r'Fail to login')
if rc == 'err_002':
    sys.exit(r'Fail to initialize QC session')

print(r'Logged in succesfully and QC session initialized')

# alm.get_defects_single()
fields = ["user-01","id","name"]
filter = r"{user-01['Osprey R4' or 'Osprey']}"

sprs = alm.get_defects_product(filter, fields, 25)


alm.logout()


# fields = ["id"]

# filter = r"{user-template-07['NC - Design Non-Conformance'];creation-time[>= '" + almBgn + r"' And < '" + almEnd + r"']}"

# sprs = alm.get_defects_info(filter, fields, 25)

# candidates = []
# for spr in sprs:
#     chs = alm.get_defect_changes(spr['id'])
#     if (chs[-1]['name'] == 'user-01') and (len(chs[-1]['src']) < 1):
#         # expected very first inialization
#         del chs[-1]
#     if len(chs) > 0:
#         if (chs[-1]['name'] == 'user-template-19') and (len(str(chs[-1]['trg'])) > 0):
#             # optional during clone initialization
#             del chs[-1]
#             if len(chs) < 1:
#                 # cloned defect expected be moved to a different bucket
#                 print('Unexpected: ' + 'cloned spr:'  + str(spr['id']) + ' not moved out')
#                 break
#             if (chs[-1]['name'] == 'user-01'):
#                 # legitimate move of the clone to different bucket
#                 del chs[-1]
#     # any following change of the 'project' bucket is a suspect
#     for ch in reversed(chs):
#         if (ch['name'] == 'user-01'):
#             # optional during clone initialization
#             candidates.append({'spr':spr['id'], 'src':ch['src'], 'trg':ch['trg']})
#         else:
#             # no other changes expected here
#             print('Unexpected: ' + str(ch) + ' of spr:'  + str(spr['id']))

# print(r"Closed QC session at " + alm.logout())
# print()
# print("----------------------------------------------------------------------------")
# print(r"Final list of " + str(len(candidates)) + r" suspect(s) for review:")
# #print("%-8s %-25s %-25s" % ('SPR', 'FROM', 'TO'))
# print("%8s %25s %25s" % ('SPR', 'FROM', 'TO'))
# for item in candidates:
#     print("%8s,%25s,%25s" % (item['spr'], item['src'], item['trg']))