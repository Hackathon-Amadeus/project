import os
from telegram.ext import *
import json
import responses as r

print("Bot started...")

data = dict()


def get_id(update):
	return update.message.chat.id


def create_fields(id):
	global data
	data[id] = {'pergunta' : 0, 'nome': '', 'CNPJ': '', 'estado' : '', 'renda' : '', 'credito' : '', 'indicador' : '', 'maturidade' : False}


def start_command(update, context):
	global data
	update.message.reply_text("Oi! Eu sou a Maria. Fico muito feliz em ver que você quer investir no seu negócio. :-D Estou aqui para te ajudar. Se você desejar, digite \"cadastro\" para iniciar o processo. Lembrando que o pré-cadastro não é garantia de acesso nem liberação de crédito, tá? ;-)")
	create_fields(get_id(update))


def help_command(update, context):
	update.message.reply_text("Então, por enquanto sou só um protótipo, realizo apenas o pré-cadastro das pessoas. Digite 'cadastro' se deseja iniciar o processo.")


def save_file(data, user_id):
	user_file = open(str(user_id), 'w')
	user_file.write(json.dumps(data[user_id]))
	user_file.flush()
	user_file.close()


def handle_message(update, context):
	text = str(update.message.text).lower()
	response = r.sample_responses(text, data[get_id(update)])
	update.message.reply_text(response)
	print(update.message.chat.id)
	print(data[get_id(update)]['pergunta'])
	if data[get_id(update)]['pergunta'] == -1:
		update.message.reply_text(json.dumps(data[get_id(update)]))
		save_file(data, get_id(update))


def error(update, context):
	print(f"Update {update} caused error {context.error}")


def main():
	updater = Updater('5807972274:AAGg0toccu0xlL8k17ywSCzslib7CC5HP-k', use_context = True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start_command))
	dp.add_handler(CommandHandler("help", help_command))

	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_error_handler(error)

	updater.start_polling()
	updater.idle()

main()