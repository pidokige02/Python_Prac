import re

zen2 = """Although never is often better than * right * now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea - - let's do more of those!"""

m = re.findall("^If", zen2, re.MULTILINE)		# ^ : start with If
print(m)

m2 = re.findall("idea\.", zen2, re.MULTILINE)	# find "idea." \. means real '.'.
print(m2)

m22 = re.findall("idea.*", zen2, re.MULTILINE)	#zere or more occurrence of any characters followed by idea
print(m22)

m3 = re.findall("idea.$", zen2, re.MULTILINE)	# $ : end with idea.
print(m3)
