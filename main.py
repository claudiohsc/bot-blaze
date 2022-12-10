import requests
import json
from decouple import config

cont_branco = False
token = ''
chat_id = ''
id_antigo = 0
cont_green, cont_loss = 0, 0

while True:

    try:
        #acessa a api e pega os dados
        pegar_dados = requests.get('https://blaze.com/api/roulette_games/recent')
        result = json.loads(pegar_dados.content)
    except NameError as erro:
        print(erro)
    except Exception as erro:
        print(erro)


    #verifica se att a ultima rodada
    ids = [x['id'] for x in result]

    if id_antigo != ids[0]:
    
        id_antigo = ids[0]
        
        #seleciona somente os numeros que sairam
        dadosbruto = [x['roll'] for x in result]
        

        finalnum = dadosbruto[0:16]


        #cria uma lista com as cores
        cor = [x['color'] for x in result]
        cores = cor[0:16]

        finalcor = []
        for num in range(len(cores)):
            if cores[num] == 1:
                finalcor.append('V')
            if cores[num] == 2:
                finalcor.append('P')
            if cores[num] == 0:
                finalcor.append('B')


        print(finalnum)
        print(finalcor)

        

        #estrategia de contagem a partir do branco   
        
        if finalcor[1] == 'B' and cont_branco == False:
            if finalnum[0] < 16:
                contagem = finalnum[0]
                cor_s = finalcor[0]
                cont_branco = True
                alerta = f'🟡 ALERTA para Estratégia Matemática do BRANCO - [Aguardar {contagem-1} rodadas] 🟡'
                url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={alerta}'
                requests.get(url)
        
        
        #verificação para mandar o sinal
        if cont_branco == True:
            if finalcor[contagem-1] == 'B':
                if cor_s == 'P':
                    sinal = '''
                        ✅ Estratégia Matemática do BRANCO [ Entrar no ⚫ ]
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={sinal}'
                    requests.get(url)
                else:
                    sinal = '''
                        ✅ Estratégia Matemática do BRANCO [ Entrar no 🔴 ]
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={sinal}'
                    requests.get(url)

            #verificação do green [estratégia branco]
            if finalcor[0] == cor_s and finalcor[contagem] == 'B':
                if cor_s == 'P':
                    cont_green += 1
                    win = f'''
                        ✅ GREEN no ⚫ - ESTRATÉGIA DO BRANCO ✅
                        Midas x Blaze
                        {cont_green} x {cont_loss}
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                    requests.get(url)
                    cont_branco = False
                else:
                    cont_green += 1
                    win = f'''
                        ✅ GREEN no 🔴 - ESTRATÉGIA DO BRANCO ✅
                        Midas x Blaze
                        {cont_green} x {cont_loss}
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                    requests.get(url)
                    cont_branco = False
            #Entrada para o gale 1
            elif finalcor[0] != cor_s and finalcor[contagem] == 'B':
                loss = '''
                        ❌ LOSS ESTRATÉGIA DO BRANCO ❌
                        '''
                url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={loss}'
                requests.get(url)
                if cor_s == 'P':
                    entrada = '''
                        ✅ Entrada no ⚫ [GALE 1] ✅
                    '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={entrada}'
                    requests.get(url)
                else:
                    entrada = '''
                        ✅ Entrada no 🔴 [GALE 1] ✅
                    '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={entrada}'
                    requests.get(url)
            
            #verificação do green GALE 1 [estratégia branco]
            if finalcor[0] == cor_s and finalcor[contagem+1] == 'B':
                if cor_s == 'P':
                    cont_green += 1
                    win = f'''
                        ✅ GREEN no ⚫ - ESTRATÉGIA DO BRANCO - [ GALE 1 ] ✅
                        Midas x Blaze
                        {cont_green} x {cont_loss}
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                    requests.get(url)
                    cont_branco = False
                else:
                    cont_green += 1
                    win = f'''
                        ✅ GREEN no 🔴 - ESTRATÉGIA DO BRANCO - [ GALE 1 ] ✅
                        Midas x Blaze
                        {cont_green} x {cont_loss}
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                    requests.get(url)
                    cont_branco = False
            elif finalcor[0] != cor_s and finalcor[contagem+1] == 'B':
                if cor_s == 'P':
                    cont_loss += 1
                    win = f'''
                        ❌ LOSS no ⚫ - ESTRATÉGIA DO BRANCO - [ GALE 1 ] ❌
                        Midas x Blaze
                        {cont_green} x {cont_loss}
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                    requests.get(url)
                    cont_branco = False
                else:
                    cont_loss += 1
                    win = f'''
                        ❌ LOSS no 🔴 - ESTRATÉGIA DO BRANCO - [ GALE 1 ] ❌
                        Midas x Blaze
                        {cont_green} x {cont_loss}
                        '''
                    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                    requests.get(url)
                    cont_branco = False


        def verificarsaida(cores):
            #compara os ultimos lances com os padroes

            if cores[0:3] == ['V', 'V', 'V']:
                return '''
                ✅ Estrategia BÁSICA [ Entrar no ⚫ ]
                '''

            if cores[0:3] == ['P', 'P', 'P']:
                return '''
                ✅ Estrategia BÁSICA [ Entrar no 🔴 ]
                '''


        #verificar ultima rodada para green ou loss
        def win_loss(padrao):

            if padrao[0:4] == ['P','V', 'V', 'V']:
                win = '''
                ✅ GREEN no ⚫ ✅
                '''
                #envia win
                url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                requests.get(url)
                return
            
            if padrao[0:4] == ['V','P', 'P', 'P']:
                win = '''
                ✅ GREEN no 🔴 ✅
                '''
                #envia win
                url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={win}'
                requests.get(url)
                return

            if padrao[0:4] == ['V','V', 'V', 'V'] or padrao[0:4] == ['B','V', 'V', 'V']:
                loss = '''
                ❌ LOSS no ⚫ ❌
                '''
                #envia loss
                url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={loss}'
                requests.get(url)
                return
            
            if padrao[0:4] == ['P','P', 'P', 'P'] or padrao[0:4] == ['B','P', 'P', 'P']:
                loss = '''
                ❌ LOSS no 🔴 ❌
                '''
                #envia loss
                url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={loss}'
                requests.get(url)
                return

        #api para enviar mensagem no telegram
        
        mensagem = verificarsaida(finalcor)
        win_loss(finalcor)

        if mensagem != None:
            url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensagem}'

            requests.get(url)

        print('Esperando próximo giro..')