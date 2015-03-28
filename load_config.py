import configparser
import sys
from error_handler import checkErrors

class ConfigLoader():
	'''
	Class to load all the configs and
	left everything ready for the
	bot
	'''

	def __init__(self):
		self.config = configparser.RawConfigParser()
		self.configset = self.config.read('config/config.cfg')
		if(len(self.configset) != 1):
			print("Could not find config.cfg")
			sys.exit()

	def getConfigTable(self):
		configTable = []
		errors = []
		
		'''
		Removido a senha do arquivo de configuracao.
		try:
			_matricula = self.config.get('USER', 'matricula')
			if(len(_matricula) != 9):
				errors.append('Matricula Invalida')
			else:
				configTable.append(_matricula)
		except: 
			errors.append('A matricula nao esta corretamente configurada')

		try:
			_senha = self.config.get('USER', 'senha')
			if(len(_senha) == 0):
				errors.append('Senha Invalida')
			else:
				configTable.append(_senha)
		except:
			errors.append('A senha nao esta corretamente configurada')
		'''

		try:
			_refreshRate = self.config.getint('WATCH', 'intervalo')
			if (_refreshRate < 2):
				print("WARNING: O intervalo e muito baixo, o bot usara 5 minutos como Default.")
				_refreshRate = 5
			configTable.append(str(_refreshRate))
		except:
			errors.append('O intervalo esta incorreto no arquivo de configuracao.')


		if ( len(errors) > 0):
			checkErrors(errors)

		self.printConfig(configTable)
		
		return configTable

	def printConfig(self, _configTable):
		print('-----------------')
		print('Configuracao carregada.')