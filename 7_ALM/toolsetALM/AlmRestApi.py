############################################################
#
# Interface Class to communicate ALM REST API 
#
############################################################
#
# Field names of Defects are following:  
# 
# 'user-01' labeled as 'Project'
# 'user-template-19' labeled as 'Cloned ID'
# 'user-13' labeled as 'DRB Reviewed'
# 'user-template-07' labeled as 'Classification'
# 'creation-time' labeled as 'Detected on Date'
#
############################################################

import json
import requests
from requests.auth import HTTPBasicAuth
import re

alm_table_map = {
    'user-01' : 'Project',
    'id' : 'Defect ID',
    'name' : 'Summary',
    'creation-time' : 'Detected on Date',
    'detected-by' : 'Detected By',
    'user-04' : 'Detected By',
    'GI Development' : 'user-template-17',
    'user-03' : 'Issue Type',
    'priority' : 'Priority',
    'user-template-07' : 'Classification',
    'user-13' : 'DRB Reviewed',
    'reproducible' : 'Reproducible',
    'user-template-01' : 'Status',
    'owner' : 'Assigned To',
    'target-rcyc' : 'Target Cycle',
    'user-template-04' : 'External Defect ID',
    'user-10' : 'Verifier',
    'user-template-09' : 'Disposition',
    'user-template-15' : 'Root Cause',
    'user-template-16' : 'Duplicate ID',
    'user-template-20' : 'Resolved By',
    'user-12' : 'Resolved in Branch or Version',
    'user-08' : 'Resolve Date',
    'user-09' : 'Verify Date',
    'user-02' : 'Category',
    'user-16' : 'Status Update',
    'user-27' : 'DRB Comments'                        
}


class AlmRestApi:
    # almURL = "https://hc-alm.health.ge.com/qcbin/"   # not a valid link @2024 
    almURL = "https://hc-alm16.cloud.health.ge.com/qcbin/"
    
    almDomain = "ULTRASOUND"
    almProject = "GI"
    midPoint = "rest/domains/" + almDomain + "/projects/" + almProject + "/"

    authEndPoint = almURL + "authentication-point/authenticate"
    qcSessionEndPoint = almURL + "rest/site-session"
    qcLogoutEndPoint = almURL + "authentication-point/logout"

    __headers = {
        'cache-control': "no-cache",
        'Accept': "application/json",
        'Content-Type': "application/json"
    }

    def __init__(self):
        self.sess = requests.Session()
        self.sess.trust_env = False
        self.cookies = dict()


    def login(self, almUsername, almPassword):
        response = self.sess.post(AlmRestApi.authEndPoint, auth=HTTPBasicAuth(almUsername, almPassword), headers=AlmRestApi.__headers, verify=False)
        if response.status_code != 200:
            return 'err_001'
        cookieName = response.headers.get('Set-Cookie')
        match = re.search(r'LWSSO_COOKIE_KEY=([^;]+)', cookieName)
        if match:
            LWSSO_COOKIE_KEY = match.group(1)
            self.cookies['LWSSO_COOKIE_KEY'] = LWSSO_COOKIE_KEY
        else:
            print("LWSSO_COOKIE_KEY를 찾을 수 없습니다.")
            return 'err_002'        
        
        response = self.sess.post(AlmRestApi.qcSessionEndPoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False)

        if (response.status_code != 200) and (response.status_code != 201):
            return 'err_002'

        cookieName = response.headers.get('Set-Cookie').split(",")[1]
        QCSession = cookieName[cookieName.index("=") + 1: cookieName.index(";")]
        self.cookies['QCSession'] = QCSession
        return None


    def logout(self):
        response = self.sess.post(AlmRestApi.qcLogoutEndPoint, headers=self.__headers, cookies=self.cookies)
        return response.headers.get('Expires')


    def get_defects_single(self):
        qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects/" + r"94173"
        # print ("jinha",qcallEndoint)
        response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False)        
        if response.status_code == 200:
            alm_entry_data = response.json()
            # print(type(alm_entry_data))
            for field in alm_entry_data['Fields']:
                field_name = field['Name']
                field_values = field['values']
                print(f"Field Name: {field_name}")
                print(f"Field Values: {field_values}")

            # print("ALM Entry Data:", alm_entry_data)
            # with open("output.json", "w") as json_file:
            #     json.dump(alm_entry_data, json_file)      
            
            # parsed_data = json.loads(alm_entry_data)
            # entry_name = parsed_data['Project']
            # print("1",entry_name)  
        else:
            print("Failed to retrieve ALM Entry. Status Code:", response.status_code)
            print("Response Content:", response.text)


    def get_defects_Osprey_R4(self, the_filter, the_fields, the_page_size):
        sufx = r"query=" + requests.utils.quote(the_filter) + r"&fields=" + requests.utils.quote(",".join(the_fields)) + "&page-size=" + str(the_page_size) + "&start-index="
        qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects/"

        sprs = []

        while True:
            qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects?" + sufx + str(len(sprs) + 1)
            response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
        
            if not ('entities' in response.keys()):
                return sprs
            for e in response['entities']:
                item = {}
                for f in e['Fields']:
                    if f['Name'] in the_fields:
                        v = []
                        for val in f['values']:
                            if 'value' in val.keys():
                                v.append(val['value'])
                        if len(v) > 0:
                            item[f['Name']] = ",".join(v)
                sprs.append(item)
            if len(response['entities']) < the_page_size:
                return sprs
        return None # never ever



    def get_defects_info(self, the_filter, the_fields, the_page_size):
        sufx = r"query=" + requests.utils.quote(the_filter) + r"&fields=" + requests.utils.quote(",".join(the_fields)) + "&page-size=" + str(the_page_size) + "&start-index="
        sprs = []
        while True:
            qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects?" + sufx + str(len(sprs) + 1)
            response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
            if not ('entities' in response.keys()):
                return sprs
            for e in response['entities']:
                item = {}
                for f in e['Fields']:
                    if f['Name'] in the_fields:
                        v = []
                        for val in f['values']:
                            if 'value' in val.keys():
                                v.append(val['value'])
                        if len(v) > 0:
                            item[f['Name']] = ",".join(v)
                sprs.append(item)
            if len(response['entities']) < the_page_size:
                return sprs
        return None # never ever

    def get_defect_changes(self, spr):
        qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/defects/" + str(spr) + r"/audits"
        response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
        actions = []
        aus = response['Audits']
        if type(aus) is dict:
            aus = [aus]
        for au in aus:
            chs = au['Audit']
            if type(chs) is dict:
                chs = [chs]
            for ch in chs:
                prs = ch['Properties']
                if type(prs) is dict:
                    prs = [prs]
                for pr in prs:
                    ups = pr['Property']
                    if type(ups) is dict:
                        ups = [ups]
                    for up in ups:
                        if str(up['Name']) in ['user-01', 'user-template-19']:
                            actions.append({'name':up['Name'], 'src':up['OldValue'], 'trg':up['NewValue']})
        return actions


