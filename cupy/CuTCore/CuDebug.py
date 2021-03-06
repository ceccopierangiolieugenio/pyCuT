import inspect

from .CuT import  CuT

class CuTMsgType(int): pass
CuTDebugMsg    = 0 # A message generated by the cuDebug() function.
CuTInfoMsg     = 4 # A message generated by the cuInfo() function.
CuTWarningMsg  = 1 # A message generated by the cuWarning() function.
CuTCriticalMsg = 2 # A message generated by the cuCritical() function.
CuTFatalMsg    = 3 # A message generated by the cuFatal() function.
CuTSystemMsg   = CuTCriticalMsg

___cuMessageHandler = None

def ___process_msg(mode, msg):
	global ___cuMessageHandler
	if ___cuMessageHandler is not None:
		curframe = inspect.currentframe()
		calframe = inspect.getouterframes(curframe,1)
		if len(calframe) > 2:
			class context():
				__slots__ = ('file', 'line', 'function')
			ctx = context()
			context.file     = calframe[2][1]
			context.line     = calframe[2][2]
			context.function = calframe[2][3]
			___cuMessageHandler(mode, context, msg)

def cuDebug(msg):
	___process_msg(CuTDebugMsg, msg)

def cuInfo(msg):
	___process_msg(CuTInfoMsg, msg)

def cuWarning(msg):
	___process_msg(CuTWarningMsg, msg)

def cuCritical(msg):
	___process_msg(CuTCriticalMsg, msg)

def cuFatal(msg):
	___process_msg(CuTFatalMsg, msg)

def cuInstallMessageHandler(mh):
	global ___cuMessageHandler
	___cuMessageHandler = mh
