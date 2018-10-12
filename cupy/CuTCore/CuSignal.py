
import inspect
import re

'''
ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
'''

# dummy decorator
def pycutSlot(*args, **kwargs):
	def pycutSlot_d(func):
		# Add signature attributes to the function
		func._cutslot_attr = args
		return func
	return pycutSlot_d

___signal_class_re = re.compile(r"^\s*class\s*[^()\s]*\s*\([^)]*\)\s*:")
___signal_class_id = 0
def pycutSignal(*args, **kwargs):
	'''
		This pile of rubbish is required to mimic the "pyqtSignal()" behaviour
		it can be used as Class or Object member and in both cases it refer
		to the object when used
	'''
	curframe = inspect.currentframe()
	calframe = inspect.getouterframes(curframe,1)
	if len(calframe) > 2:
		if ___signal_class_re.match(calframe[2][4][0]):
			# It's a Class Member
			global ___signal_class_id
			___signal_class_id += 1
			# Create a unique name to identify this Signal in the object
			idx = '___cusignal_eu___'+str(___signal_class_id)
			def tmp_prop(self):
				if hasattr(self, idx):
					tmp_ret = getattr(self, idx)
				else:
					tmp_ret = pycutSignal_obj(*args, **kwargs)
					setattr(self, idx, tmp_ret)
				return tmp_ret
			ret = property(tmp_prop)
		else:
			# It's NOT a Class Member
			ret = pycutSignal_obj(*args, **kwargs)
	del calframe
	del curframe
	return ret

class pycutSignal_obj():
	'''
		ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#PyQt5.QtCore.pyqtSignal

		PyQt5.QtCore.pyqtSignal(types[, name[, revision=0[, arguments=[]]]])
			Create one or more overloaded unbound signals as a class attribute.

			Parameters:
			types - the types that define the C++ signature of the signal. Each type may be a Python type object or a string that is the name of a C++ type. Alternatively each may be a sequence of type arguments. In this case each sequence defines the signature of a different signal overload. The first overload will be the default.
			name - the name of the signal. If it is omitted then the name of the class attribute is used. This may only be given as a keyword argument.
			revision - the revision of the signal that is exported to QML. This may only be given as a keyword argument.
			arguments - the sequence of the names of the signal's arguments that is exported to QML. This may only be given as a keyword argument.
			Return type:
				an unbound signal
	'''
	__slots__ = ('_types', '_name', '_revision', '_connected_slots')
	def __init__(self, *args, **kwargs):
		self._types = args
		self._name = kwargs.get('name', None)
		self._revision = kwargs.get('revision', 0)
		self._connected_slots = []

	'''
		ref: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#connect

		connect(slot[, type=PyQt5.QtCore.Qt.AutoConnection[, no_receiver_check=False]]) -> PyQt5.QtCore.QMetaObject.Connection
			Connect a signal to a slot. An exception will be raised if the connection failed.

			Parameters:
			slot - the slot to connect to, either a Python callable or another bound signal.
			type - the type of the connection to make.
			no_receiver_check - suppress the check that the underlying C++ receiver instance still exists and deliver the signal anyway.
			Returns:
				a Connection object which can be passed to disconnect(). This is the only way to disconnect a connection to a lambda function.
	'''
	def connect(self, slot):
		if hasattr(slot, '_cutslot_attr') and slot._cutslot_attr != self._types:
			error = "Decorated slot has no signature compatible: "+slot.__name__+str(slot._cutslot_attr)+" != signal"+str(self._types)
			raise TypeError(error)
		self._connected_slots.append(slot)

	def disconnect(self, *args, **kwargs):
		for slot in args:
			self._connected_slots.remove(slot)

	def emit(self, *args, **kwargs):
		if len(args) != len(self._types):
			error = "func"+str(self._types)+" signal has "+str(len(self._types))+" argument(s) but "+str(len(args))+" provided"
			raise TypeError(error)
		for slot in self._connected_slots:
			slot(*args, **kwargs)
