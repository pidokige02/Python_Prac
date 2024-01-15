import sys
import getpass
import warnings

from  Scripts.AlmRestApi import AlmRestApi
from  Scripts.almtable import *
from  Scripts.export2excel import *


# -------------------------------------------------------------------
# make following as a user input:
# almUsername = input(r"Enter ALM username: ")
# almPassword =  getpass.getpass(r"Enter ALM password: ")
almUsername="jin ha.hwang"
almPassword="oct1006minja"
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
# sprs = alm.get_defects_Osprey_R4(filter, fields, 25)
# # print("jinha", sprs)
# spr2excel(sprs,alm_table_header)
##################################################################


##################################################################
## fetch the whole defect entities for Osprey R4 Oprey for feasibility testing.
fields = list(alm_table_map.keys())
# filter = r"{user-01['Osprey R4' or 'Osprey']}"
filter = r"{user-01['Gemini R4']}"
sprs = alm.get_defects_Osprey_R4(filter, fields, 25)
spr2excel(sprs,alm_table_header)
##################################################################

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