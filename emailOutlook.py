'''
Módulo que abre a lista completa de contatos do Tribunal de Justiça e insere apenas
os contatos das varas cíveis no dicionário 'contatos'
'''


def listaDeEmails(contatos):
    emails = list()

    try:
        file = open('listaComarcas.csv')
        comarcas = file.readlines()
    except:
        print('Não conseguiu abrir o arquivo de e-mails.')
        return
    else:
        file.close()
        #print(comarcas)
    

    for linha in comarcas:
        #print(linha)
        linha = linha.split(';')
        for i in range(0, len(linha)):
            emails.append(linha[i])
            #print(emails)
        if linha[0] == 'UPJ' and linha[1] in ('JOAO MENDES SANTO AMARO'):
            for j in range(int(linha[2]), (int(linha[3])+1)):
                contatos[f'{linha[1]}'][j] = linha[4]
            emails.clear()
        else:
            contatos[f'{linha[0]}'] = emails[:]
            emails.clear()
    
    return(contatos)

#--------------------
# Área de testes
#--------------------
#enderecos = dict()
#listaDeEnderecos(enderecos)
#==================================================================================

#------------------------------------------------------------#
#   ABRE O ARQUIVO DE E-MAILS                                #
#------------------------------------------------------------#
def abreTXT():
    while True:
        try:
            #Recebe e testa o nome do arquivo. Ex. de nome:'mensagemEmail2'
            nomeArquivo = input('Digite o nome do arquivo:\n')
            file = open(nomeArquivo + '.txt')
        except:
            #Mostra a mensagem se o python não conseguir abrir o arquivo
            print('Nome do arquivo inválido!!!\n')
        else:
            #Salva o conteúdo do arquivo na variável arquivo
            arquivo = file.read()
            file.close()
            return(arquivo)
        
#arquivo = abreTXT()

def separaMsg(arquivo):
    return(arquivo.split('+-+'))

#listaDeMensagens = separaMsg(arquivo)

#------------------------------------------------------------#
#   TRATAMENTO DA MENSAGEM                                   #
#------------------------------------------------------------#
def separaForo(foroOrigem):
    '''
    Recebe o no completo do foro de origem.
    Ex: 'FORO DE AGUAÍ'; 'FORO CENTRAL CÍVEL'
    
    Retorna o nome que está na lista de contatos.
    Ex: 'AGUAI'; 'JOAO MENDES'
    '''
    
    acentuadas = ('Á', 'É', 'Í', 'Ó', 'Ú', 'Â', 'Ê', 'Ô', 'Ã', 'Õ', 'Ü', 'Ç')
    semAcento = ('A', 'E', 'I', 'O', 'U', 'A', 'E', 'O', 'A', 'O', 'U', 'C')
    if 'REGIONAL' in foroOrigem:
        if 'BUTANTÃ' in foroOrigem:
            foro = 'BUTANTA'
            return(foro)
        elif 'PENHA DE FRANÇA' in foroOrigem:
            foro = 'PENHA DE FRANCA'
            return(foro)
        elif 'LAPA' in foroOrigem:
            foro = 'LAPA'
            return(foro)
        elif 'VILA MIMOSA' in foroOrigem:
            foro = 'VILA MIMOSA'
            return(foro)
        elif 'NOSSA SENHORA' in foroOrigem:
            foro = 'NOSSA SENHORA DO O'
            return(foro)
        elif 'FAZENDA PUBLICA' in foroOrigem:
            foro = 'HELY LOPES MEIRELLES'
            return(foro)
        else:
            foroOrigem = foroOrigem.split(' DE ')
            foro = foroOrigem[-1].strip()
            for i in range(len(acentuadas)):
                foro = foro.replace(acentuadas[i], semAcento[i])
            return(foro)

    elif 'CENTRAL CÍVEL' in foroOrigem:
        foro = 'JOAO MENDES'
        return(foro)
    
    elif 'FAZENDA PÚBLICA' in foroOrigem:
        foro = 'HELY LOPES MEIRELLES'
        return(foro)

    else:
        foroOrigem = foroOrigem.split(' DE ')
        #print(foroOrigem)
        foro = foroOrigem[-1].strip()
        for i in range(len(acentuadas)):
            foro = foro.replace(acentuadas[i], semAcento[i])
        return(foro)


def oficio(vara):
    '''
    Recebe o número ordinal da vara (3ª, 5ª).
    Retorna apenas o nº inteiro, que é o indíce da lista de contatos.
    '''
    vara = vara.upper()
    if vara == 'VARA':
        return(1)
    elif vara == 'SETOR UNIFICADO DE CARTAS PRECATÓRIAS CÍVEIS':
        return(1)
    else:
        vara = vara.split('ª')
        if len(vara) == 1:
            vara = vara[0].split('º')
            if len(vara) == 1:
                vara = vara[0].split('°')
                if len(vara) == 1:
                    vara = vara[0].split('.')
                    oficio = vara[0]
                    return(oficio)
                oficio = vara[0]
                return(oficio)
            oficio = vara[0]
            return(oficio)
        oficio = vara[0]
        return(oficio)

#------------------------------------------------------------#
#   ACESSANDO O ENDERECO NO DATAFRAME                        #
#------------------------------------------------------------#
def enderecoVO(foro, vara):
    endereco = contatos[foro][vara]
    return(endereco)


def infoMsg():
    for k in range(1, len(listaDeMensagens)):
        listaTemp.clear()
    # copia um e-mail que está na posição k para a variável mensagem
        mensagem = listaDeMensagens[k]
    # separa o e-mail em 4 partes: Foro, Vara, Assunto e Corpo
        mensagem = mensagem.split('$$$')
    # Encaminha o foro para a funcao separaForo() que retorna o nome ajustado e sem acentos           
        foro = mensagem[0].upper()
        foro = separaForo(foro)
    # Separa e armazena apenas o nº da vara. 
        vara = mensagem[1].split()
        vara = vara[0]
        print(k, vara, end='\t')
        vara = oficio(vara)
    #print(vara, end='\t')
        vara = int(vara)
        print(foro)
    # Solicita para a funcao endereco o enderecoVO() de e-mail da vara
        endereco = enderecoVO(foro, vara)
        listaTemp.append(endereco)
    # copia o assunto do e-mail
        assunto = mensagem[2]
        listaTemp.append(assunto)
    # copia o corpo do e-mail
        corpo = mensagem[3]
        listaTemp.append(corpo)
        listaDeEnvio.append(listaTemp[:])
        
        
#listaDeEnvio = []
#listaTemp = []
#infoMsg()

#------------------------------------------------------------#
#   ENVIANDO O E-MAIL                                        #
#------------------------------------------------------------#
def envioOutlook():
    #integração com o outlook
    outlook = win32.Dispatch('outlook.application')
     
    for i in range(len(listaDeEnvio)):
        print(listaDeEnvio[i][0], end='\t\t')
        # cria um item do outlook
        email = outlook.CreateItem(0)
        # configurar o e-mail
        email.To = listaDeEnvio[i][0]
        email.Subject = listaDeEnvio[i][1]
        email.Body = listaDeEnvio[i][2]
        email.Send()
        print("Enviado")

import win32com.client as win32

# 1) Carrega os endereços de e-mail das varas
contatos = dict()
listaDeEmails(contatos)

# 2) Abre o arquivo '.TXT'
arquivo = abreTXT()

# 3) Separa cada uma das mensagens. As mensagens que estão na variável arquivo são separadas pelos caracteres '+-+'
listaDeMensagens = separaMsg(arquivo)

# 4) Gera a listaDeEnvio com as informações de cada mensagem na listaDeMensagens
    # 4.1) Separa foro
    # 4.2) Vara (oficio)
    # 4.3) Endereço VO
listaDeEnvio = []
listaTemp = []
infoMsg()

# 5) Enviando o e-mail
envioOutlook()

# 6) Fim do programa
print('E-mails enviados')
input('Aperte uma tecla para sair')
