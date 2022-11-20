
#from telegram.ext import *
#from    main.py import * 

# Verificação de digitos
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# Verificação de letras
def has_alpha(inputString):
    return any(char.alpha() for char in inputString)
# Verificação de data
def is_data(inputString):
    if len(inputString) < 10:
        return 0;
    if not inputString[0].isdigit():
        return 0;
    if not inputString[1].isdigit():
        return 0;
    if not inputString[2].isdigit():
        return 0;
    if not inputString[3].isdigit():
        return 0;
    if inputString[4] != '-':
        return 0;
    if not inputString[5].isdigit():
        return 0;
    if not inputString[6].isdigit():
        return 0;
    if inputString[7] != '-':
        return 0;
    if not inputString[8].isdigit():
        return 0;
    if not inputString[9].isdigit():
        return 0;
    return 1;

# teste api
from amadeus import Client, ResponseError,  Location

amadeus = Client(
    client_id='oGDkd7G61c0KfkmVV3oAQtMNryvoW6VG',
    client_secret='GwXAbyPUziKZC8S9'
)


# Logica responsável por selecionar as respostas. Ela toma como input
# a resposta do usuário e verifica se não tem nenhum erro grotesco.
# Caso esteja tudo ok, o usuário recebe a próxima pergunta, caso contrário,
# uma mensagem de erro é exibida até que ele coloque uma resposta adequada.
def sample_responses(input_text, data):
    user_message = str(input_text).lower()

    if "go" in user_message:
        data['pergunta'] = 1
        return "Perfeito! De que cidade você quer partir?(Me diga o código IATA do aeroporto que você quer sair, eu ainda estou em um estágio bem inicial de desenvolvimento...)"
    elif data['pergunta'] == 1:
        if has_numbers(user_message):
            data['pergunta'] = 1
            return "Nem eu que sou uma robô tenho números no meu nome. o__O Tente digitar o nome correto de sua cidade."
        else:
            data.update({'src':user_message})
            data['pergunta'] += 1
            return "Agora, o aeroporto de destino. (Só entendo códigos IATA por enquanto...)😅"
    elif data['pergunta'] == 2:
        if has_numbers(user_message):
            data['pergunta'] = 2
            return "Somente o nome da cidade, por favor."
        else:
            data.update({'dest': user_message})
            data['pergunta'] += 1
            #teste = amadeus.reference_data.locations.get(
            #       keyword=user_message,
            #        subType=Location.CITY,
            #        )
            #print(teste.data)'''
            return "Qual o código do seu país. Ex: Brasil -> BR, França -> FR, Estados Unidos -> US"
    elif data['pergunta'] == 3:
        if user_message in ("br, fr, us, pr, ca, it, pt, en"):
            data.update({'contrycode': user_message})
            data['pergunta'] += 1
            return "É um lugar lindo! 😍Já estamos na metade! Quantos adultos irão nessa viagem contando com você?"
        else:
            data['pergunta'] == 3
            return "Não reconheço esse código x__x Digite um código valido"
    elif data['pergunta'] == 4:
        if user_message.isdigit() is False:
            data['pergunta'] = 4
            return "Somente os dígitos, por favor. ;-)"
        else:
            data.update({'adults': user_message})
            data['pergunta'] += 1
            return "Muito bem, agora eu preciso saber que dia você espera estar partindo! Digite data no seguinte formato ano-mes-dia. ex:2022-12-25 (Então é natal, HO HO HO!)"
    elif data['pergunta'] == 5:
        if is_data(user_message) == 0:
            data['pergunta'] = 5
            return "Somente uma data válida será aceita. ;-)"
        else:
            data.update({'data': user_message})
            data['pergunta'] += 1
        try:
            response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=data['src'].upper(),
            destinationLocationCode=data['dest'].upper(),
            departureDate=data['data'].upper(),
            adults=1)
        except ResponseError as error:
            print(error) 
        price = float(response.data[0]['price']['grandTotal']) * 5
        return ("O preço da passagem ficou em " + str(price) + " Reais.\nTem interesse em seguros de saúde? Responda com \"sim\" ou \"não\".")
    elif data['pergunta'] == 6:
        data.update({'upsell': user_message})
        data['pergunta'] += 1
        return "Para terminar! Você pretende ficar por mais de 6 meses? Responda com \"sim\" ou \"não\"."
    elif data['pergunta'] == 7:
        data['pergunta'] = -1
        if user_message in ("sim", "s"):
            data.update({'Permanence': True})
        else:
            data.update({'Permanence': False})
            print(data)
        return "Prontinho! Já terminamos! Obrigada pelas respostas. Aguarde o retorno de seu pedido em seu email 😄"
