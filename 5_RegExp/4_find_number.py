import re

string = "123?45yy7890 hi 999 hello"

m1 = re.findall("\d", string)		# ‘\d’ 은 숫자
m2 = re.findall("[0-9]{1,2}", string)	#[0-9]:0부터9까지 {1,2}: 1글자에서 2글자.
m3 = re.findall("[1-5]{1,2}", string)	#[1-5]:1부터5까지 {1,2}: 1글자에서 2글자.

print("m1=", m1)
print("m2=", m2)
print("m3=", m3)
