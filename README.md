# Chat-IRC-de-Terminal

Projeto de redes de computadores na qual foi implementado um chat usando pyhton

Foi feito um bate papo na internet se baseando no protocolo Internet Relay Chat (IRC),
mas aqui foi utilizado apenas um servidor local que não pode se conectar com outros canais.
Quando o usuário entrar no servidor será pedido seu nick e seu nome real.
Os comandos presentes no servidor são:
NICK <nome> : trocar o nickname do usuário
QUIT : para encerrar a aplicação
JOIN <nome> : entra em um canal, caso o canal não exista será criado um
PART <nome> : sairá do canal
LIST : listará todos os canais disponíveis separado por espaço 
PRIVMSG <nome1>, <nome2>, ... : <msg> : enviará uma mensagem privada para os nomes informados, se for um usuário,
ele irá receber a mensagem privada. Caso o nome for um canal, a mensagem será enviada no canal (mesmo o usuário não sendo do canal)
WHO <nome> : se o nome for um usuário será informado o canal que o nome está. Caso o nome for um canal será informado todos presente nesse canal
