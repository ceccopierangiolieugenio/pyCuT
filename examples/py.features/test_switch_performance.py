from timeit import timeit
import re



a = 123
b = 567
c = 234
d = 456
e = 345

lookup = {
		a: a + 1,
		b: b + 2,
		c: c + 3,
		d: d + 4,
		e: e + 5,
	}
def func_switch(val):
	return lookup.get(val,0)

def test_switch():
	ret  = func_switch(a)
	ret += func_switch(b)
	ret += func_switch(c)
	ret += func_switch(d)
	ret += func_switch(e)
	return ret

def func_ifelse(val):
	if   val == a: return a + 1
	elif val == b: return b + 2
	elif val == c: return c + 3
	elif val == d: return d + 4
	elif val == e: return e + 5

def test_ifelse():
	ret  = func_ifelse(a)
	ret += func_ifelse(b)
	ret += func_ifelse(c)
	ret += func_ifelse(d)
	ret += func_ifelse(e)
	return ret

print test_ifelse()
print test_switch()

print timeit("test_switch()",   "from __main__ import test_switch;")
print timeit("test_ifelse()",   "from __main__ import test_ifelse;")
