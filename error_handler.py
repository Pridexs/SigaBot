import sys

def checkErrors(errors):
	print('-----------------')
	while (len(errors) > 0):
		printError(errors.pop())
	print('-----------------')
	print('Exiting bot...')
	sys.exit()

def printError(_error):
	print('ERROR: ' + _error)

	