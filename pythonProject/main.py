import os
from telegram.ext import *
import json
import responses as r
from amadeus import Client, ResponseError, Location

amadeus = Client(
    client_id='API KEY',
    client_secret='API KEY SECRET'
)

print("Bot started...")

data = dict()

def get_id(update):
    return update.message.chat.id

def create_fields(id):
    global data
    data[id] = {'pergunta' : 0, 'src': '', 'dest': '', 'contrycode' : '', 'adults' : '', 'data' : '', 'upsell' : '', 'Permanence' : False}

def start_command(update, context):
    global data
    update.message.reply_text("Seja bem vindo ao seu Concierge. Vamos iniciar a sua jornada nômade? Digite 'go' para encontrar o vôo que te levará ao seu próximo destino!")
    create_fields(get_id(update))

def help_command(update, context):
    update.message.reply_text("Então, por enquanto sou só um protótipo, realizo a simulação de compra de uma passagem aérea.")

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = r.sample_responses(text, data[get_id(update)])
    update.message.reply_text(response)
    print(update.message.chat.id)
    print(data[get_id(update)]['pergunta'])

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater('API KEY', use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()
