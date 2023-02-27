import re

string = "aaaaaaa<hr>This</hr>"

# pattern = re.compile("<(.*)>")
# 소괄호 ( 은 찾고자 하는 문자 시작을 의미한다.

pattern = re.compile("(<.*>)") #<hr>This</hr>

mm = re.findall(pattern, string)
print(mm)

for m in re.finditer(pattern, string):  #pattern 을 () 로 묶어주니까 find 가 되었다.
    print(m.groups())
