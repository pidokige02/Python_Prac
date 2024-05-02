import json
import requests
from requests.auth import HTTPBasicAuth
import sys,os,re 

from .Utils import *
from .almtable import *


class AlmRestApi:
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
		qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects/" + r"91389"
        # print ("jinha",qcallEndoint)
		result_dict = {}

		response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False)        
		if response.status_code == 200:
			alm_entry_data = response.json()
            # print(type(alm_entry_data))
			for field in alm_entry_data['Fields']:
				field_name = field['Name']
				field_values = field['values']
				result_dict[field_name] = field_values

			print("ALM Entry Data:", alm_entry_data)
			with open("output.json", "w") as json_file:
				json.dump(alm_entry_data, json_file)      
            
            # parsed_data = json.loads(alm_entry_data)
            # entry_name = parsed_data['Project']
            # print("1",entry_name)
			return result_dict  
		else:
			print("Failed to retrieve ALM Entry. Status Code:", response.status_code)
			print("Response Content:", response.text)


	def get_defects_product(self, the_filter, the_fields, the_page_size):
		sufx = r"query=" + requests.utils.quote(the_filter) + r"&fields=" + requests.utils.quote(",".join(the_fields)) + "&page-size=" + str(the_page_size) + "&start-index="
		qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects/"

		sprs = []
		print("start Fetching ALM entries!!")
		
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
							if 'value' and 'ReferenceValue' in val.keys():
								v.append(val['ReferenceValue'])
							if 'value' in val.keys() and not 'ReferenceValue' in val.keys():
								v.append(val['value'])	
						# if len(v) > 0:  # 중간에 data가 없는 field 가 skip 되어 표시되지 않는 문제를 해결함
						item[f['Name']] = ",".join(v)
				sprs.append(item)
			if len(response['entities']) < the_page_size:
				return sprs
		return None # never ever

	# def get_defects_info(self, the_filter, the_fields, the_page_size):
	# 	sufx = r"query=" + requests.utils.quote(the_filter) + r"&fields=" + requests.utils.quote(",".join(the_fields)) + "&page-size=" + str(the_page_size) + "&start-index="
	# 	sprs = []
	# 	while True:
	# 		qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects?" + sufx + str(len(sprs) + 1)
	# 		response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 		if not ('entities' in response.keys()):
	# 			return sprs
	# 		for e in response['entities']:
	# 			item = {}
	# 			for f in e['Fields']:
	# 				if f['Name'] in the_fields:
	# 					v = []
	# 					for val in f['values']:
	# 						if 'value' in val.keys():
	# 							v.append(val['value'])
	# 					if len(v) > 0:
	# 						item[f['Name']] = ",".join(v)
	# 			sprs.append(item)
	# 		if len(response['entities']) < the_page_size:
	# 			return sprs
	# 	return None # never ever

	# def get_defect_changes(self, spr):
	# 	qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/defects/" + str(spr) + r"/audits"
	# 	response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	actions = []
	# 	aus = response['Audits']
	# 	if type(aus) is dict:
	# 		aus = [aus]
	# 	for au in aus:
	# 		chs = au['Audit']
	# 		if type(chs) is dict:
	# 			chs = [chs]
	# 		for ch in chs:
	# 			prs = ch['Properties']
	# 			if type(prs) is dict:
	# 				prs = [prs]
	# 			for pr in prs:
	# 				ups = pr['Property']
	# 				if type(ups) is dict:
	# 					ups = [ups]
	# 				for up in ups:
	# 					if str(up['Name']) in ['user-01', 'user-template-19']:
	# 						actions.append({'name':up['Name'], 'src':up['OldValue'], 'trg':up['NewValue']})
	# 	return actions
		
	# def get_field_metadata(self):
	# 	qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"customization/entities/Defect/fields"
	# 	response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	if response.get("Fields") is None:
	# 		return
	# 	fields = response.get("Fields").get("Field")
	# 	if fields is None:
	# 		return
	# 	labelInfo = {}
	# 	for field in fields:
	# 		label = field.get("label")
	# 		if label is not None and label in labelInfo:
	# 			printWarning("Duplicate label names found.")
	# 		labelInfo.update({field.get("name"):field.get("label")})
	# 	return labelInfo
	
	# def get_user_details(self):
	# 	qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/customization/users"
	# 	response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	if response.get("users") is None:
	# 		return
	# 	users = response.get("users")
	# 	#print(users)
	# 	userInfo = {}
	# 	for user in users:
	# 		if (user.get("UserActive") is False or user.get("email") == "" or user.get("email") is None):
	# 			continue
	# 		name = user.get("Name")
	# 		if name is not None and name in userInfo:
	# 			printWarning("Duplicate names found.")
	# 		userInfo.update({name:user.get("email")})
	# 	#print(userInfo)
	# 	return userInfo
		   
	def get_favorite_filter_id(self, filter_name):
			sufx = r"query={"+ (requests.utils.quote(f"name['{filter_name}']")) + "}"
			qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/favorites?" + sufx
			response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
			
			if response.get("entities") is None :
				return
			filter_id = None
			favorites = response.get("entities")
			if len(favorites) > 1:
				printError(f"Duplicate values present for the favorite '{filter_name}' in ALM. Change the filter name in ALM and try again")
				sys.exit()
			for fav in favorites: 
				nameFound = False
				for field in fav.get("Fields"):
					if nameFound == False and "name" == field.get("Name") and filter_name == field.get("values")[0].get("value"):
						nameFound = True
					if nameFound == True and "id" == field.get("Name"):
						filter_id = field.get("values")[0].get("value")
			return filter_id
	  
	# def create_filter_query(self, filter_id):
	# 	qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/favorites/{}".format(filter_id)
	# 	response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	#print(response)
	# 	if response.get("Filter") is None and response.get("Filter").get("Where"):
	# 		return
	# 	query = None
	# 	queryData = []
	# 	where = response.get("Filter").get("Where").get("Field")
	# 	for condition in where:
	# 		field = condition.get("Name")
	# 		value = condition.get("Value")
	# 		if "id" == field and "or" in value and len(value)>1000 :
	# 			value = value.lower()
	# 			value=value.replace('"',"")
	# 			value=value.replace("'","")
	# 			value=value.replace(" ","")
	# 			spridList = value.split("or")
	# 			spridList.sort()
	# 			#print(len(spridList))
	# 			spridList = list(set(spridList))
	# 			#spridList = list(map(int, spridList))
	# 			value = " or ".join(spridList)
				
	# 		if '"' in value:
	# 			value=value.replace('"',"'")
	# 			queryData.append( "{}[{}]".format(field,value))
	# 		else:
	# 			queryData.append( "{}[{}]".format(field,value))
	# 	if len (queryData) > 0:
	# 		query = ";".join(queryData)
		
	# 	return r"{}".format(query)
	
	# def fav_filter_columns(self, filter_id):
	# 	qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/favorites/{}".format(filter_id)
	# 	response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	if response.get("Layout") is None and response.get("Layout").get("VisibleColumns"):
	# 		return
	# 	queryData = []
	# 	columns = response.get("Layout").get("VisibleColumns")
	# 	for column in columns:
	# 		field = column.get("Name")
	# 		queryData.append(field)
		
	# 	return queryData
		
	# def fav_filter_columns_actual_name(self, filter_id):
	# 	qcalltestEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"/favorites/{}".format(filter_id)
	# 	response = self.sess.get(qcalltestEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	if response.get("Layout") is None and response.get("Layout").get("VisibleColumns"):
	# 		return
	# 	queryData = []
	# 	columns = response.get("Layout").get("VisibleColumns")
	# 	metadata=self.get_field_metadata()
	# 	for column in columns:
	# 		field = column.get("Name")
	# 		queryData.append(metadata.get(field))
		
	# 	return queryData
		
	def get_defects_by_filter_name(self, filter_name, the_page_size=1000):
		filter_id=self.get_favorite_filter_id(filter_name)
		rel_ids = self.get_all_release_ids()
		cycle_ids = self.get_all_cycle_ids()
		if filter_id is None:
			printError("'{}' not found in the favorites".format(filter_name))
			sys.exit()
		filter_query = self.create_filter_query(filter_id)
		filter_columns = self.fav_filter_columns(filter_id)
		metadata = self.get_field_metadata()
		#print(filter_query)
		sufx = r"query={" + filter_query + r"}&fields=" + requests.utils.quote(",".join(filter_columns)) + "&page-size=" + str(the_page_size) + "&order_by=id" +  "&start-index="
		sprs = []
		while True:
			qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"defects?" + sufx + str(len(sprs) + 1)
			response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False)
			'''
			print(qcallEndoint)
			print(len(qcallEndoint))			
			print(response.status_code)
			print(f"Content : {response.reason}")
			print(dir(response))
			'''
			response = response.json()
			if response.get("entities") is None:
				return
			for e in response['entities']:
				item = {}
				for f in e['Fields']:
					if f['Name'] in filter_columns:
						v = []
						for val in f['values']:
							if 'value' in val.keys():
								v.append(val['value'])
						if len(v) > 0:
							if metadata.get(f['Name']) =="Target Cycle":
								item[metadata.get(f['Name'])] = cycle_ids.get(",".join(v))
							elif metadata.get(f['Name']) =="Target Release":
								item[metadata.get(f['Name'])] = rel_ids.get(",".join(v))
							else:
								item[metadata.get(f['Name'])] = ",".join(v)
				sprs.append(item)
			if len(response['entities']) < the_page_size:
				return sprs
		return None # never ever
			
	# def get_url_response(self,url):
	# 	qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + url
	# 	response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
	# 	print(qcallEndoint)		
	# 	print(response)
		
	def get_all_cycle_ids(self, the_page_size=1000):
		filter_columns = ['id','name']
		sufx = r"fields=" + requests.utils.quote(",".join(filter_columns)) + "&page-size=" + str(the_page_size) + "&order_by=id" +  "&start-index="
		cycle_ids = {}
		while True:
			qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"release-cycles?" + sufx + str(len(cycle_ids) + 1)
			#print(qcallEndoint)
			response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
			#print(response)
			if response.get("entities") is None:
				return
			for e in response['entities']:
				item = {}
				for f in e['Fields']:
					if f['Name'] in filter_columns:
						v = []
						for val in f['values']:
							if 'value' in val.keys():
								v.append(val['value'])
						if len(v) > 0:
							item[f['Name']] = ",".join(v)
				cycle_ids.update({item.get("id"):item.get("name")})
			if len(response['entities']) < the_page_size:
				return cycle_ids
		return None # never ever			
			
	def get_all_release_ids(self, the_page_size=1000):
		filter_columns = ['id','name']
		sufx = r"fields=" + requests.utils.quote(",".join(filter_columns)) + "&page-size=" + str(the_page_size) + "&order_by=id" +  "&start-index="
		rel_ids = {}
		while True:
			qcallEndoint = AlmRestApi.almURL + AlmRestApi.midPoint + r"releases?" + sufx + str(len(rel_ids) + 1)
			#print(qcallEndoint)
			response = self.sess.get(qcallEndoint, headers=AlmRestApi.__headers, cookies=self.cookies, verify=False).json()
			#print(response)
			if response.get("entities") is None:
				return
			for e in response['entities']:
				item = {}
				for f in e['Fields']:
					if f['Name'] in filter_columns:
						v = []
						for val in f['values']:
							if 'value' in val.keys():
								v.append(val['value'])
						if len(v) > 0:
							item[f['Name']] = ",".join(v)
				rel_ids.update({item.get("id"):item.get("name")})
			if len(response['entities']) < the_page_size:
				return rel_ids
		return None # never ever			 
			
