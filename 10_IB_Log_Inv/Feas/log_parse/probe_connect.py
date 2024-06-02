import re

# 주어진 문자열
text = "CHouseKeeping::HandleProbeEvent: Probe connection event conn 1 name L312L-RS (ID 457)"

# 정규표현식 패턴
pattern = r'conn (\d+) name (\S+)'

# 정규표현식을 사용하여 패턴을 검색하고 추출
match = re.search(pattern, text)

if match:
    connection = match.group(1)
    name = match.group(2)
    print("Connection:", connection)
    print("Name:", name)
else:
    print("Pattern not found.")
