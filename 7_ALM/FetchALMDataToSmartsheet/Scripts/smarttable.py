###################################################################################
# GEUK creted function
# 열의 타입을 지정할 수 있습니다. 예: TEXT_NUMBER, CONTACT_LIST, DATE, CHECKBOX 등
alm_table_map_ss = [
	{
		'title' : 'Project',
		'type': 'TEXT_NUMBER',
		'index': 0,
		'columnID' : 0
	},  
	{
		'title' : 'Defect ID',
		'type': 'TEXT_NUMBER',
		'index': 1,
		'columnID' : 0
	},  
	{
		'title' : 'Summary',
		'type': 'TEXT_NUMBER',
		'index': 2,
		'columnID' : 0
	},  
	{
		'title' : 'Detected on Date',
		'type': 'DATE',
		'index': 3,
		'columnID' : 0
	},  
	{
		'title' : 'Detected By',
		'type': 'TEXT_NUMBER',
		'index': 4,
		'columnID' : 0
	}, 
	{
		'title' : 'SW Revision & Build',
		'type': 'TEXT_NUMBER',
		'index': 5,
		'columnID' : 0
	}, 
	{
		'title' : 'GI Development',
		'type': 'PICKLIST',
		'index': 6,
		'columnID' : 0
	}, 
	{
		'title' : 'Issue Type',
		'type': 'PICKLIST',
		'index': 7,
		'columnID' : 0
	}, 
	{
		'title' : 'Priority',
		'type': 'PICKLIST',
		'index': 8,
		'columnID' : 0
	}, 
	{
		'title' : 'Classification',
		'type': 'PICKLIST',
		'index': 9,
		'columnID' : 0
	}, 
	{
		'title' : 'DRB Reviewed',
		'type': 'PICKLIST',
		'index': 10,
		'columnID' : 0
	}, 
	{
		'title' : 'Reproducible',
		'type': 'PICKLIST',
		'index': 11,
		'columnID' : 0		
	}, 
	{
		'title' : 'Status',
		'type': 'PICKLIST',
		'index': 12,
		'columnID' : 0		
	}, 
	{
		'title' : 'Assigned To',
		'type': 'CONTACT_LIST',
		'index': 13,
		'columnID' : 0		
	}, 
	{
		'title' : 'Target Cycle',
		'type': 'TEXT_NUMBER',
		'index': 14,
		'columnID' : 0		
	}, 
	{
		'title' : 'External Defect ID',
		'type': 'TEXT_NUMBER',
		'index': 15,
		'columnID' : 0		
	}, 
	{
		'title' : 'Verifier',
		'type': 'TEXT_NUMBER',
		'index': 16,
		'columnID' : 0		
	}, 
	{
		'title' : 'Disposition',
		'type': 'PICKLIST',
		'index': 17,
		'columnID' : 0		
	}, 
	{
		'title' : 'Root Cause',
		'type': 'TEXT_NUMBER',
		'index': 18,
		'columnID' : 0		
	}, 
	{
		'title' : 'Duplicate ID',
		'type': 'TEXT_NUMBER',
		'index': 19,
		'columnID' : 0		
	}, 
	{
		'title' : 'Resolved By',
		'type': 'TEXT_NUMBER',
		'index': 20,
		'columnID' : 0		
	}, 
	{
		'title' : 'Resolved in Branch or Version',
		'type': 'TEXT_NUMBER',
		'index': 21,
		'columnID' : 0		
	}, 
	{
		'title' : 'Resolve Date',
		'type': 'DATE',
		'index': 22,
		'columnID' : 0		
	}, 
	{
		'title' : 'Verify Date',
		'type': 'DATE',
		'index': 23,
		'columnID' : 0		
	}, 
	{
		'title' : 'Category',
		'type': 'TEXT_NUMBER',
		'index': 24,
		'columnID' : 0		
	}, 
	{
		'title' : 'Status Update',
		'type': 'TEXT_NUMBER',
		'index': 25,
		'columnID' : 0		
	}, 
	{
		'title' : 'DRB Comments',
		'type': 'TEXT_NUMBER',
		'index': 26,
		'columnID' :  0		
	}, 
	{
		'title' : 'Comments',
		'type': 'TEXT_NUMBER',
		'index': 27,
		'columnID' : 0		
	}, 
	{
		'title' : 'T2/Common?',
		'type': 'PICKLIST',
		'index': 28,
		'columnID' : 0		
	}, 
	{
		'title' : 'Triage',
		'type': 'PICKLIST',
		'index': 29,
		'columnID' : 0		
	}, 
]


# display name, field name, hide flag  
smart_table_header = {
    'A' : ['Project', False],
    'B' : ['Defect ID', False],
    'C' : ['Summary', False],
    'D' : ['Detected on Date', True],
    'E' : ['Detected By', True],
    'F' : ['SW Revision & Build', True],
    'G' : ['GI Development', True],
    'H' : ['Issue Type', True],
    'I' : ['Priority', True],
    'J' : ['Classification', False],
    'K' : ['DRB Reviewed', True],
    'L' : ['Reproducible', True],
    'M' : ['Status', False],
    'N' : ['Assigned To', False],
    'O' : ['Target Cycle', True],
    'P' : ['External Defect ID', True],
    'Q' : ['Verifier', True],
    'R' : ['Disposition', True],
    'S' : ['Root Cause', False],
    'T' : ['Duplicate ID', True],
    'U' : ['Resolved By', True],
    'V' : ['Resolved in Branch or Version', True],
    'W' : ['Resolve Date', True],
    'X' : ['Verify Date', True],
    'Y' : ['Category', False],
    'Z' : ['Status Update', False],
    'AA' : ['DRB Comments', True],
    'AB' : ['Comments', True],
    'AC' : ['T2/Common?', True],
    'AD' : ['Triage', True],
}
