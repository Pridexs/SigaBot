import sys
import requests
import time
import getpass
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
        self.matricula = ''
        self.senha = ''

        print('Inicializado.')

    def startBot(self):
        isBotActive = True
        nChecks = 1
        refreshRate = 0
        notas = {}
        loggedIn = False

        refreshRate = int(self.configTable[0])
        print('Refresh rate: ' + str(refreshRate) + ' minutos.')

        print('Iniciando o bot...')
        print('Tentando efetuar login...')
        
        while(not loggedIn):
            print('-----------------')
            self.matricula = input('Entre sua matricula: ')
            self.senha = getpass.getpass('Entre sua senha: ')
            if (not self.login()):
                print("Erro ao efetuar Login!")
            else:
                print("Login efetuado!")
                loggedIn = True

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
        #Iniciar os cookies e etc
        r = self.session.get('http://siga.udesc.br/siga/inicial.do')
        #URL que efetua efetivamente o login
        URL = 'http://siga.udesc.br/siga/j_security_check'
        #Data para enviar no post
        login_data = {
            'j_username': self.matricula,
            'senha': self.senha,
            'j_password': self.senha,
            'btnLogin' : '',
        }
        #Executa login
        r = self.session.post(URL, data = login_data)
        # Checa se login foi efetuado chechando o response header
        if (self.checkLogin(r.headers.keys())):
            return True
        else:
            return False        

    def checkLogin(self, keys):
        #Se ha uma key 'set-cookie' o login foi realmente efetuado.
        if ('set-cookie' in keys):
            return True

        return False

    def logout(self):
        print("Efetuando logout.")
        r = self.session.get('http://siga.udesc.br/siga/plc/desconectaPlc.do?evento=Desconectar')

    def getNotas(self):
        #Entra na pagina que contem as medias semestrais
        r = self.session.get('http://siga.udesc.br/siga/com/executaconsultapersonaliz.do?evento=executaConsulta&id=2&exe=S')
        tree = html.fromstring(r.text)

        materias = {}
        #Itera na tabela de notas, pegando todas as materias e suas respectivas medias
        for elem_a in tree.xpath('//*[@id="resultado"]/center/table/tr'):
            #Verificador de seguranca, para nao pegar valores que nao nos interessam.
            if (len(elem_a) > 1 and elem_a[0].text is not None):
                #Se nao ha nenhuma nota disponivel, atribua o valor -1 para aquela materia
                if (elem_a[2].text is None):
                    materias[elem_a[0].text] = -1.0
                #Caso tenha alguma nota, troque a virgula por um ponto e realize a conversao para float.
                else:
                    materias[elem_a[0].text] = float(elem_a[2].text.replace(',', '.'))

        #Impressao da table de media/materia
        print("")
        for a in materias:
            print(a + " - " + str(materias[a]))
        print("")
        
        return materias

    def verificaAlteracoes(self, materias_old, materias_new):
        houveAlteracao = False
        for key in materias_old:
            #Simples checage se houve alteracao
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