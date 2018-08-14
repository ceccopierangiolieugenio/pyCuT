import inspect
import pprint
import re

pp = pprint.PrettyPrinter()

# class_re = re.compile(r"^\s*class\s*[^()\s]*\s*([^)]*)\s*:")
class_re = re.compile(r"^\s*class\s*[^()\s]*\s*\([^)]*\)\s*:")
def pippo():
	curframe = inspect.currentframe()
	calframe = inspect.getouterframes(curframe,1)
	print("Len: "+str(len(calframe)))
	print("FIx:  "+ str(inspect.getframeinfo(curframe)))
	#for f in calframe:
	#	print(str(f))
		# print(str(calframe.index(f))+")-> FI:  "+ str(inspect.getframeinfo(f[0])))
	# pp.pprint(inspect)
	# pp.pprint(curframe)
	# pp.pprint(calframe)
	print('caller name: '+ calframe[1][3])

	print('LAST:     '+calframe[-1][4][0])
	if len(calframe) > 2:
		print('RetTrace: '+calframe[2][4][0])
		if class_re.match(calframe[2][4][0]):
			print("It's a Class Member")
		else:
			print("It's NOT a Class Member")
	del calframe
	del curframe
	return 1

def pippo_check():
	curframe = inspect.currentframe()
	calframe = inspect.getouterframes(curframe,1)
	# pp.pprint(calframe)
	print calframe[1][0]
	print calframe[1][1]
	print calframe[1][2]
	print calframe[1][3]
	if len(calframe) > 2:
		if class_re.match(calframe[2][4][0]):
			print("It's a Class Member")
		else:
			print("It's NOT a Class Member")
	del calframe
	del curframe
	return 1

def pluto():
	pippo_check()
	return 1

class paperino():
	a = pippo_check()

	class topolino( int ):
		d = pippo_check()
		def __init__(self):
			self.e = pippo_check()

	def __init__(self):
		self.b = pippo_check()
		self.c = self.topolino()

pippo_check()
pluto()

paperino()
paperino.topolino()