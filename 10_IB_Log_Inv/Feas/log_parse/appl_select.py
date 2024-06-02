import re

# 주어진 문자열
text = "SetApplication(ES:Abdomen)"

# 정규표현식 패턴
pattern = r'SetApplication\(ES:(\w+)\)'

# 정규표현식을 사용하여 패턴을 검색하고 추출
match = re.search(pattern, text)

if match:
    value = match.group(1)
    print("Extracted:", value)
else:
    print("Pattern not found.")
