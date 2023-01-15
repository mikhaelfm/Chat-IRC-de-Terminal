from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class Canal:
    def __init__(self, nome):
        self.nome = nome
        self.membros = []

canais =[]
membros_atuais = []
comandos_n_implementados = ['MODE', 'TOPIC', 'NAMES', 'INVITE', 'KICK', 'VERSION', 'STATS', 'LINKS', 'TIME', 'CONNECT', 'TRACE', 'ADMIN', 'INFO', 'NOTICE', 'WHOIS', 'WHOWAS', 'KILL', 'PING', 'PONG', 'ERROR']

class Usuario:
    def __init__(self, sock , endereco):
        self.sock = sock
        self.endereco = endereco[0]
        self.nome = None
        self.nome_real = None
        self.canal = None
        membros_atuais.append(self)

    
    def recv(self):
        return self.sock.recv(buffer_size).decode('utf8')
    
    def send(self, msg):
        try:
            self.sock.send(msg.encode())
        except Exception:
            del_usuario(self)
            
    
    def mudar_nick(self, nome):
        if not nome.isalnum():
            self.send('Error: Seu nome deve conter apenas letras e numero sem espaços.')
        elif nome in [usuario.nome for usuario in membros_atuais] or nome in achar_nomes_canais().split(' '):
            self.send('Error: Este nome já está em uso.')
        else:
            if self.nome == None:               
                self.nome = nome
            else:
                self.send('Seu novo nome de usuário é ' + nome + '.')
                self.enviar_canal(self.nome + 'mudou seu nome para' + nome + '.')
                self.nome = nome

    def mudar_nome(self, nome):
        self.nome_real = nome

    
    def enviar_canal(self, msg):
        if self.canal != None:
            for usuario in self.canal.membros:
                if self != usuario:
                    usuario.send(msg)


def del_usuario(usuario):
    if usuario.canal != None:
        usuario.enviar_canal(bcolors.FAIL + usuario.nome + ' saiu do chat' + bcolors.RESET)
        if usuario in usuario.canal.membros:
            usuario.canal.membros.remove(usuario)
    if usuario in membros_atuais:
        membros_atuais.remove(usuario)
    usuario.sock.close()

def achar_nomes_canais():
    temp = ''
    for canal in canais:
        temp += canal.nome + ' '
    return temp

def conexao_entrada():
    while True:
        cliente, endereco_cliente = server.accept()
        usuario = Usuario(cliente, endereco_cliente)
        print(f'{usuario.endereco} se conectou.')
        Thread(target=lidar_com_usuario, args=(usuario,)).start()

def lidar_com_usuario(usuario):
    while usuario.nome == None:
        try: 
            usuario.send('Bem-vindo, por favor digite o seu nick.')
            tentativa_nick = usuario.recv()
            usuario.send('Bem-vindo, por favor digite o seu nome.')
            tentativa_nome = usuario.recv()
        except Exception:
            print(usuario.endereco, 'teve a conexão perdida.')
            return
        usuario.mudar_nick(tentativa_nick)
        usuario.mudar_nome(tentativa_nome)
    usuario.send('Bem-vindo ' + usuario.nome)

    while True:
        try:
            msg = usuario.recv()
        except Exception:
            print(usuario.endereco + ' foi desconectado.')
            del_usuario(usuario)
            break
        if msg[0:5] == 'NICK ':
            try:
                usuario.mudar_nick(msg[5:])
            except Exception:
                pass

        elif (msg == 'USER'):
            NotImplemented

        elif (msg == 'QUIT'):
            usuario.send('')
            del_usuario(usuario)

        elif (msg[0:5] == 'JOIN '):
            canal_existe = False
            if len(canais) != 0:
                for canal in canais:
                    if canal.nome == msg[5:]:
                        canal_existe = True
                        if usuario.canal == None:
                            usuario.canal = canal
                            canal.membros.append(usuario)
                            usuario.enviar_canal(bcolors.WARNING + usuario.nome + ' entrou do chat' + bcolors.RESET)

                        elif usuario.canal == canal:
                            usuario.enviar_canal(bcolors.FAIL + usuario.nome + ' saiu do chat' + bcolors.RESET)
                            usuario.canal = None
                            canal.membros.remove(usuario)

                        else:
                            usuario.enviar_canal(bcolors.FAIL + usuario.nome + ' saiu do chat' + bcolors.RESET)
                            canais[canais.index(usuario.canal)].membros.remove(usuario)
                            usuario.canal = None
                            usuario.canal = canal
                            canal.membros.append(usuario)
                            usuario.enviar_canal(bcolors.WARNING + usuario.nome + ' entrou do chat' + bcolors.RESET)
                        break

                if not canal_existe:
                    canais.append(Canal(msg[5:]))
                    if (usuario.canal != None):
                        usuario.enviar_canal(bcolors.FAIL + usuario.nome + ' saiu do chat' + bcolors.RESET)
                        usuario.canal.membros.remove(usuario)
                    usuario.canal = canais[len(canais)-1]
                    canais[len(canais)-1].membros.append(usuario)
            else:
                canais.append(Canal(msg[5:]))
                usuario.canal = canais[0]
                canais[0].membros.append(usuario)

        elif (msg[:5] == 'PART '):
            if usuario.canal != None and usuario.canal.nome == msg[5:]:

                usuario.enviar_canal(bcolors.FAIL + usuario.nome + ' saiu do chat' + bcolors.RESET)
                canais[canais.index(usuario.canal)].membros.remove(usuario)
                usuario.canal = None
            else:            
                nomes = achar_nomes_canais()
                nomes = nomes.split(' ')
                if msg[5:] in nomes:
                    usuario.send('Você não está nesse canal.')
                else:
                    usuario.send('Este canal não existe.')

        elif (msg == 'LIST'):
            nomes = achar_nomes_canais()
            usuario.send(nomes)

        elif (msg[:8] == 'PRIVMSG '):
            if ':' in msg:
                nomes, mensagem = msg[8:].split(':')
                achou = False
                nomes_canais = achar_nomes_canais()
                nomes_canais = nomes_canais.split(' ')
                nomes = nomes.split(' ') 
                for i in nomes:
                    for j in membros_atuais:
                        if i == j.nome:
                            j.send(bcolors.OK + 'PRIVMSG ' + usuario.nome + ':' + bcolors.RESET + mensagem)
                            achou = True
                    if i in nomes_canais:
                        for membro in canais[nomes_canais.index(i)].membros:
                            membro.send(bcolors.OK + 'PRIVMSG ' + usuario.nome + ':' + bcolors.RESET + mensagem)
                            achou = True
                if not achou:
                    usuario.send('Nome não encontrado.')
            else:
                usuario.send('Formado do comando incorreto.')

        elif (msg[:4] == 'WHO '):
            nomes_canais = achar_nomes_canais()
            procura = msg[4:]
            if procura in nomes_canais:
                nomes_membros = ''
                for canal in canais:
                    if procura == canal.nome:
                        i = 4
                        for membro in canal.membros:
                            if i != 0:
                                nomes_membros += membro.nome + ' '
                                i -= 1
                            else:
                                i = 4
                                nomes_membros += membro.nome + '\n'
                        usuario.send('Usuários online no canal  ' + canal.nome + ':')
                        usuario.send(nomes_membros)
                        break

            else:
                achou = False
                for membro in membros_atuais:
                    if procura == membro.nome:
                        achou = True
                        if membro.canal == None:
                            usuario.send('O Usúario ' + membro.nome + ' está online porém não está em nenhum canal' + '.')
                        else:
                            usuario.send('O Usúario ' + membro.nome + ' está online no canal ' + membro.canal.nome + '.')
                if not achou:
                    usuario.send('Nome não encontrado.')
        elif (msg.split(' ')[0] in comandos_n_implementados):
            usuario.send('ERR UNKNOWNCOMMAND')
        else:
            if (usuario.canal != None):
                usuario.send('{:>80}'.format(msg))
                usuario.enviar_canal(bcolors.OK + usuario.nome + ': ' + bcolors.RESET + msg)    
            else:
                pass

    

        

host = '192.168.2.94'
porta = 6668
buffer_size = 1500

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((host, porta))

server.listen(10)

print('Servidor iniciado.')
thread = Thread(target=conexao_entrada)
thread.start()
thread.join()
server.close()