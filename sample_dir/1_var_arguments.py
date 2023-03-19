def fn():
	print("fn called")
def exp(x):
	return x ** 2
def get_fruits():
	return ['오렌지', '사과', '바나나']
def get_name():
	return 'Kent', 'Beck'

fn()
print(exp(2))
print(get_fruits())
print(get_name())


def var_param(a, *vp):
    print(a, len(vp), vp[len(vp) - 1])
var_param(1, 2, 3, 4)

def set_dic_param(*argv, **kargv):
	print("set params=", len(argv), '<--', argv)
	print("dic params=", kargv.keys(), '<--', kargv)
set_dic_param(1, 2, 3, name='hong', age=23)


def default_param(a, vp = 100):
    print(a, vp)

default_param(1)