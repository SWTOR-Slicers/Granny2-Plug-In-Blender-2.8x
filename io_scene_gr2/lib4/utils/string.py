# <pep8 compliant>

import os

from .binary import DataView


def path_format(head, tail):
	# type: (str, str) -> str
	if os.name == 'nt':
		filepath = head[:head.rfind('\\')] + tail.replace('/', '\\')
	else:
		filepath = head[:head.rfind('/')] + tail.replace('\\', '/')
	return filepath


def path_split(path):
	# type: (str) -> str
	if os.name == 'nt':
		filename = path.split('\\')[-1]
	else:
		filename = path.split('/')[-1]
	return filename


def readString(dv, posIn, posOverride=None):
	# type: (DataView, int, int|None) -> str
	
	pos = None
	if posOverride is None:
		pos = dv.getUint32(posIn, True)
	else:
		pos = posOverride
	
	outString = ""
	curChar = dv.getUint8(pos)
	pos += 1

	while curChar != 0:
		outString += chr(curChar)
		curChar = dv.getUint8(pos)
		pos += 1

	return outString


def readCString(dv, pos):
	# type: (DataView, int) -> str
	outString = ""
	curChar = dv.getUint8(pos)
	pos += 1

	while curChar != 0:
		outString += chr(curChar)
		curChar = dv.getUint8(pos)
		pos += 1

	return outString
