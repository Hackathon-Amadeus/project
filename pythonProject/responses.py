# Verificação de digitos
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# Verificação de letras
def has_alpha(inputString):
    return any(char.alpha() for char in inputString)

# Logica responsável por selecionar as respostas. Ela toma como input
# a resposta do usuário e verifica se não tem nenhum erro grotesco.
# Caso esteja tudo ok, o usuário recebe a próxima pergunta, caso contrário,
# uma mensagem de erro é exibida até que ele coloque uma resposta adequada.
def sample_responses(input_text, data):
	user_message = str(input_text).lower()


	if "go" in user_message:
		data['pergunta'] = 1
		return "Perfeito! De que cidade você quer partir?"
	elif data['pergunta'] == 1:
		if has_numbers(user_message):
			data['pergunta'] = 1
			return "Nem eu que sou uma robô tenho números no meu nome. o__O Tente digitar o nome correto de sua cidade."
		else:
			data.update({'src':user_message})
			data['pergunta'] += 1
			return "Agora o nome da cidade de seu destino, mas sem pontos nem traços, por favor. :-)"
	elif data['pergunta'] == 2:
		if has_numbers(user_message):
			data['pergunta'] = 2
			return "Somente o nome da cidade, por favor."
		else:
			data.update({'dest': user_message})
			data['pergunta'] += 1
			return "Qual o código do seu país. Ex: Brasil -> BR, França -> FR, Estados Unidos -> US"
	elif data['pergunta'] == 3:
		if user_message in ("br, fr, us, pr, ca, it, pt, en"):
			data.update({'contrycode': user_message})
			data['pergunta'] += 1
			return "É um lugar lindo! \*___\* Já estamos na metade! Quantos adultos irão nessa viagem contando com você?"
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
		if user_message.isdigit() is True:
			data['pergunta'] = 5
			return "Somente os dígitos, por favor. Sem cifras, sem centavos e sem vírgula. ;-)"
		else:
			data.update({'data': user_message})
			data['pergunta'] += 1
			return "Tem interesse em seguros de saúde? Responda com \"sim\" ou \"não\"."
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
		return "Prontinho! Já terminamos! Obrigada pelas respostas. Agora vamos conectar você à instituição que mais combina com o seu perfil. Aguarde o retorno deles em alguns dias, beleza? Abraços, vou ficando por aqui! :-D"
	if user_message in ("oi", "ola", "olá"):
					return "Olááá! :-D"
