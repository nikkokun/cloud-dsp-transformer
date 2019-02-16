import os

def stretch(src,factor):
	print('Applying stretch (factor: {})'.format(factor))
	return os.path.join('output','transformed.wav')

def pitchShift(src,shift):
	print('Applying pitch shift (shift: {})'.format(shift))
	return os.path.join('output','transformed.wav')

def percussive(src,param):
	print('Applying percussive: ({})'.format(param))
	return os.path.join('output','transformed.wav')

def harmonic(src,param):
	print('Applying harmonic (param: {})'.format(param))
	return os.path.join('output','transformed.wav')

def dj(src,param):
	print('Applying dj (param: {})'.format(param))
	return os.path.join('output','transformed.wav')
