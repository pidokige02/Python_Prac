import re

string = "Beautiful is better than ugly.\
Explicit is better than implicit.\
Simple is better than complex.\
Complex is better than complicated.\
Flat is better than nested.\
Sparse is better than dense.\
Readability counts.\
Special cases aren't special enough to break the rules.\
Although practicality beats purity.\
Errors should never pass silently.\
Unless explicitly silenced.\
In the face of ambiguity, refuse the temptation to guess.\
There should be one-- and preferably only one --obvious way to do it.\
Although that way may not be obvious at first unless you're Dutch.\
Now is better than never.\
Although never is often better than *right* now.\
If the implementation is hard to explain, it's a bad idea.\
If the implementation is easy to explain, it may be a good idea.\
Namespaces are one honking great idea -- let's do more of those!"

# pattern = re.compile('of+')
# mm = re.findall(pattern, string)
# print(mm)

# pattern = re.compile('[a-z]+')  # 소문자로 시작하는 모든 단어를 찾아준다.
# mm = re.findall(pattern, string)
# print(mm)


# pattern = re.compile('[a-z]+')      # 소문자로 시작하는 모든 단어를 찾아준다.
# m = pattern.match("python")         #문자열의 처음부터 정규식과 매치되는지 조사
# print(m)

# p = re.compile('[a-z]+')
# m = p.match('string goes here')
# if m:
#     print('Match found: ', m.group())
# else:
#     print('No match')

# p = re.compile('[a-z]+')
# m = p.search("3 python")  # 문자열 전체를 검색하여 정규식과 매치되는지 조사
# print(m)

# p = re.compile('[a-z]+')
# result = p.findall("life is too short")
# print(result)

# p = re.compile('[a-z]+')
# result = p.finditer("life is too short")  # 정규식과 매치되는 모든 문자열(substring)을 반복 가능한 객체로 리턴
# print(result)
# for r in result:
#     print(r)

# p = re.compile('[a-z]+')
# m = p.match("python")
# print(m.group())
# print(m.start())
# print(m.end())
# print(m.span())

# p = re.compile('[a-z]+')
# m = p.search("3 python")
# print(m.group())
# print(m.start())
# print(m.end())
# print(m.span())


# p = re.compile('Crow|Servo') # | 메타 문자는 or과 동일한 의미
# m = p.match('CrowHello')
# print(m)

# print(re.search('^Life', 'Life is too short')) #^ 메타 문자는 문자열의 맨 처음과 일치함을 의미

# print(re.search('^Life', 'My Life'))

# print(re.search('short$', 'Life is too short'))  #$는 문자열의 끝과 매치함

# print(re.search('short$', 'Life is too short, you need python'))

# p = re.compile(r'\bclass\b')  # \b는 단어 구분자, 단어는 whitespace에 의해 구분
# # 백스페이스가 아닌 단어 구분자임을 알려 주기 위해 r'\bclass\b'처럼 Raw string임을 알려주는 기호 r을 반드시 붙여 주어야
# print(p.search('no class at all'))
# print(p.search('the declassified algorithm'))

# p = re.compile(r'\Bclass\B')    # \B 메타 문자는 \b 메타 문자와 반대 whitespace로 구분된 단어가 아닌 경우에만 매치
# print(p.search('no class at all'))
# print(p.search('the declassified algorithm'))
# print(p.search('one subclass is'))


# 그룹을 만들어 주는 메타 문자는 바로 ( )이다.
# p = re.compile('(ABC)+')
# m = p.search('ABCABCABC OK?')
# print(m)
# print(m.group())

# \d - 숫자와 매치, [0-9]와 동일한 표현식
# \D - 숫자가 아닌 것과 매치, [^0-9]와 동일한 표현식
# \s - whitespace 문자와 매치, [ \t\n\r\f\v]와 동일한 표현식이다. 맨 앞의 빈 칸은 공백문자(space)를 의미
# \S - whitespace 문자가 아닌 것과 매치, [^ \t\n\r\f\v]와 동일한 표현식
# \w - 문자+숫자(alphanumeric)와 매치, [a-zA-Z0-9_]와 동일한 표현식
# \W - 문자+숫자(alphanumeric)가 아닌 문자와 매치, [^a-zA-Z0-9_]와 동일한 표현식

# Dot(.) 메타 문자는 줄바꿈 문자인 \n을 제외한 모든 문자와 매치
# a.b   => "a + 모든문자 + b"
# a[.]b => "a + Dot(.)문자 + b"
# *은 * 바로 앞에 있는 문자 a가 0부터 무한대로 반복
# +는 최소 1번 이상 반복
# ca{2}t => "c + a(반드시 2번 반복) + t".
# ca{2,5}t => "c + a(2~5회 반복) + t"
# ab?c => "a + b(있어도 되고 없어도 된다) + c"

# p = re.compile(r"\w+\s+\d+[-]\d+[-]\d+")
# m = p.search("park 010-1234-1234")
# print(m)

# 반복되는 문자열을 찾을 때 그룹을 사용하는데, 그룹을 사용하는 보다 큰 이유는 위에서 볼 수 있듯이 매치된 문자열 중에서
# 특정 부분의 문자열만 뽑아내기 위해서
# p = re.compile(r"\w+\s+\d+[-]\d+[-]\d+")
# m = p.search("park 010-1234-1234 lee 010-9001-6667")
# print(m.group())  # 0 이나 blank 이외의 다른 index 는 동작하지 않았다.

# pattern = re.compile(r"\w+\s+\d+[-]\d+[-]\d+")
# mm = re.findall(pattern, "park 010-1234-1234 lee 010-9001-6667")
# print(mm)
# print(mm[0])
# print(mm[1])

# pattern = re.compile(r"(\w+\s+\d+[-]\d+[-]\d+)")
# for m in re.finditer(pattern, "park 010-1234-1234 lee 010-9001-6667"):
#     print(m.groups())

# txt = "The rain in Spain"
# x = re.search(r"\bS\w+", txt)
# print(x.group(0))

# p = re.compile('(blue|white|red)')
# x = p.sub('colour', 'blue socks and red shoes')
# print(x)

# p = re.compile('(blue|white|red)')
# x = p.subn('colour', 'blue socks and red shoes')  # return value is tuple type
# print(x)


p = re.compile(r"(?P<name>\w+)\s+(?P<phone>(\d+)[-]\d+[-]\d+)")
print(p.sub("\g<phone> \g<name>", "park 010-1234-1234"))

# p = re.compile(r"(?P<name>\w+)\s+(?P<phone>(\d+)[-]\d+[-]\d+)")
# print(p.sub("\g<2> \g<1>", "park 010-1234-1234"))
