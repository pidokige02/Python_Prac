# Select One and None

import re

string = "Two aa too"

# m = re.findall("t[ow]o", string)		#[ow] : ‘o’ or ‘w’
m = re.findall("t[ow]o", string, re.IGNORECASE)
print(m)


m = re.findall("t[^w]o", string, re.IGNORECASE)		#[]안의 ^은 NOT임
print(m)
