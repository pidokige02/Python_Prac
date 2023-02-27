import re
line = "Beautiful is better than ugly."
matches = re.findall("Beautiful", line)
print(matches)


matches2 = re.findall("beautiful", line, re.IGNORECASE)
print(matches2)
