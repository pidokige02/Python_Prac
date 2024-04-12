import sys
import getpass
import warnings

from AlmRestApi import AlmRestApi

# -------------------------------------------------------------------
# make following as a user input:
almUsername = input(r"Enter ALM username: ")
almPassword =  getpass.getpass(r"Enter ALM password: ")
almTarget = input(r"Enter ALM Project bucket: ")
# -------------------------------------------------------------------

warnings.simplefilter("ignore")

alm = AlmRestApi()

rc = alm.login(almUsername, almPassword)
if rc == 'err_001':
    sys.exit(r'Fail to login')
if rc == 'err_002':
    sys.exit(r'Fail to initialize QC session')

print(r'Logged in succesfully and QC session initialized')

fields = ["id", "user-template-19", "user-13"]

filter = r"{user-01['" + almTarget + r"']}"

sprs = alm.get_defects_info(filter, fields, 25)

candidates = []
backref = {}

for spr in sprs:
    if (not "user-13" in spr.keys()) or (spr["user-13"] != 'Y'):
        if not ("user-template-19" in spr.keys()):
            candidates.append(spr['id'])
        else:
            backref[spr['user-template-19']] = spr['id']

print()
print("----------------------------------------------------------------------------")
print(r"Found " + str(len(candidates)) + r" candiates for DRB at level of the Project's bucket (total " + str(len(sprs)) + r" SPRs)")
print("----------------------------------------------------------------------------")
print()

while len(backref.keys()) > 0:
    print()
    print("----------------------------------------------------------------------------")
    print(r"Digging deeper to following sources of clones SPRs:")
    print(",".join(backref.keys()))
    print("----------------------------------------------------------------------------")
    print()
    query = r"{id['" + "' or '".join(backref.keys()) + r"']}"
    sprs = alm.get_defects_info(query, fields, 25)
    loc_backref = {}
    for spr in sprs:
        if (not "user-13" in spr.keys()) or (spr["user-13"] != 'Y'):
            if not ("user-template-19" in spr.keys()):
                candidates.append(backref[spr['id']])
            else:
                loc_backref[spr['user-template-19']] = backref[spr['id']]
    backref = loc_backref

print(r"Closed QC session at " + alm.logout())        
print()
print("----------------------------------------------------------------------------")
print(r"Final list of " + str(len(candidates)) + r" candiates for DRB:")
print(",".join(candidates))