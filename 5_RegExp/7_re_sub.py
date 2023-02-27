import re

string = "https://aaa.bbb.com/"

x = re.sub("(http(s)*|:|/)", '', str)

print(x)