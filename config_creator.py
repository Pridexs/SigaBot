import configparser

config = configparser.ConfigParser()
config['USER'] = { 'Matricula' : 'sua_matricula_aqui',
                    'Senha' : 'sua_senha_aqui' }

config['WATCH'] = { 'Intervalo' : '5.4' }

with open('config/config.cfg', 'w') as configfile:
    config.write(configfile)
