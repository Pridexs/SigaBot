import sys
import requests
import time
from lxml import etree
from lxml import html
from load_config import ConfigLoader

class Bot():
    '''
    Main bot class
    '''

    def __init__(self):
        self.config_loader = ConfigLoader()
        self.configTable = self.config_loader.getConfigTable()
        self.session = requests.Session()
        print('Inicializado.')

    def startBot(self):
        isBotActive = True
        nChecks = 1
        refreshRate = 0
        notas = {}

        refreshRate = int(self.configTable[2])
        print('Refresh rate: ' + str(refreshRate) + ' minutos.')

        print('Iniciando o bot...')
        print('Tentando efetuar login...')
        
        if (not self.login()):
            print("Erro ao efetuar Login!")
            return False
        else:
            print("Login efetuado!")

        #Pega as notas iniciais.
        notas = self.getNotas()

        while (isBotActive):
            print ("Check [%d]: %s" % (nChecks,time.ctime()))
            nChecks = nChecks + 1
            notas_new = self.getNotas()
            #Enquanto ele nao achar alteracoes, continue checando.
            isBotActive = not self.verificaAlteracoes(notas, notas_new)
            time.sleep(refreshRate * 60)

        self.logout()
        print('Exiting.')
        return True

    def login(self):
        r = self.session.get('http://siga.udesc.br/siga/inicial.do')
        URL = 'http://siga.udesc.br/siga/j_security_check'
        login_data = {
            'j_username': self.configTable[0],
            'senha': self.configTable[1],
            'j_password': self.configTable[1],
            'btnLogin' : '',
        }
        r = self.session.post(URL, data = login_data)

        if (self.checkLogin(r.headers.keys())):
            return True
        else:
            return False        

    def checkLogin(self, keys):
        if ('set-cookie' in keys):
            return True

        return False

    def logout(self):
        print("Efetuando logout.")
        r = self.session.get('http://siga.udesc.br/siga/plc/desconectaPlc.do?evento=Desconectar')

    def getNotas(self):
        r = self.session.get('http://siga.udesc.br/siga/com/executaconsultapersonaliz.do?evento=executaConsulta&id=2&exe=S')

        tree = html.fromstring(r.text)

        materias = {}
        for elem_a in tree.xpath('//*[@id="resultado"]/center/table/tr'):
            if (len(elem_a) > 1 and elem_a[0].text is not None):
                if (elem_a[2].text is None):
                    materias[elem_a[0].text] = -1.0
                else:
                    materias[elem_a[0].text] = float(elem_a[2].text.replace(',', '.'))

        print("")
        for a in materias:
            print(a + " - " + str(materias[a]))
        print("")
        
        return materias

    def verificaAlteracoes(self, materias_old, materias_new):
        houveAlteracao = False
        for key in materias_old:
            if(materias_old[key] != materias_new[key]):
                print("A MEDIA DE " + key + " FOI ALTERADA!")
                print("A NOVA MEDIA EH: " + str(materias_new[key]))
                print("A MEDIA NAO NECESSARIAMENTE EQUIVALE A NOVA NOTA MODIFICADA. VERIFIQUE SUA NOTA EM NOTAS PARCIAIS!")
                houveAlteracao = True
        return houveAlteracao


if __name__ == '__main__':
    print("Iniciando o bot...")
    bot = Bot()
    bot.startBot()
