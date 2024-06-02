import re

# 주어진 문자열
text = "EchoRootPck::PowerOffRack"

# 정규표현식 패턴
pattern = r'EchoRootPck::PowerOffRack'

# 정규표현식을 사용하여 패턴을 검색하고 추출
match = re.search(pattern, text)

if match:
    value = match.group()
    print("Extracted:", value)
else:
    print("Pattern not found.")
