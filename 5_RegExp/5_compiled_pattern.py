import re

string = "123?45yy7890 hi 999 hello"

# pattern = re.compile("[0-9]{1,3}")	#[0-9]:0부터9까지 {1,3}: 1글자에서 3글자.
pattern = re.compile("(\d{1,3})")	#숫자중 {1,3}: 1글자에서 3글자.
# print(pattern)


mm = re.findall(pattern, string)   # mm 은 list type
print(mm)

for m in re.finditer(pattern, string): # m은 tuple type
    print(m.groups())
