alm_table_map = {
    'user-01' : 'Project',
    'id' : 'Defect ID',
    'name' : 'Summary',
    'creation-time' : 'Detected on Date',
    'detected-by' : 'Detected By',
    'user-04' : 'SW Revision & Build',
    'user-15' : 'GI Development',
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
    'user-27' : 'DRB Comments',                        
}

alm_table_map_for_link = {
    'user-01' : 'Project',
    'id' : 'Defect ID',
    'name' : 'Summary',
    'user-template-19' : 'Cloned ID'
}

# display name, field name, hide flag  
alm_table_header = {
    'A' : ['Project', 'user-01', False],
    'B' : ['Defect ID', 'id', False],
    'C' : ['Summary', 'name', False],
    'D' : ['Detected on Date','creation-time', True],
    'E' : ['Detected By','detected-by', True],
    'F' : ['SW Revision & Build','user-04', True],
    'G' : ['GI Development','user-15', True],
    'H' : ['Issue Type','user-03', True],
    'I' : ['Priority','priority', True],
    'J' : ['Classification','user-template-07', False],
    'K' : ['DRB Reviewed','user-13', True],
    'L' : ['Reproducible','reproducible', True],
    'M' : ['Status','user-template-01', False],
    'N' : ['Assigned To', 'owner', False],
    'O' : ['Target Cycle','target-rcyc', True],
    'P' : ['External Defect ID','user-template-04', True],
    'Q' : ['Verifier','user-10', True],
    'R' : ['Disposition','user-template-09', True],
    'S' : ['Root Cause','user-template-15', False],
    'T' : ['Duplicate ID','user-template-16', True],
    'U' : ['Resolved By','user-template-20', True],
    'V' : ['Resolved in Branch or Version', 'user-12', True],
    'W' : ['Resolve Date','user-08', True],
    'X' : ['Verify Date','user-09', True],
    'Y' : ['Category','user-02', False],
    'Z' : ['Status Update','user-16', False],
    'AA' : ['DRB Comments','user-27', True],                        
}


# display name, field name, hide flag  
alm_link_table_header = {
    'A' : ['Project', 'user-01', False],
    'B' : ['Defect ID', 'id', False],
    'C' : ['Summary', 'name', False],
    'D' : ['Detected on Date','user-template-19', False],
}
