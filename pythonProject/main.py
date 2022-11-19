import os
from telegram.ext import *
import json
import responses as r
from amadeus import Client, ResponseError

amadeus = Client(
    client_id='oGDkd7G61c0KfkmVV3oAQtMNryvoW6VG',
    client_secret='GwXAbyPUziKZC8S9'
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='LON',
        destinationLocationCode='ATH',
        departureDate='2022-12-01',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)

try:
    response = amadeus.reference_data.recommended_locations.get(cityCodes='LON', travelerCountryCode='US')
    #print(response.data)
except ResponseError as error:
    print(error)

objeto = response.data
lat  = objeto[0]['geoCode']['latitude']
lon = objeto[0]['geoCode']['longitude']

response = amadeus.safety.safety_rated_locations.get(latitude=(lat), longitude= (lon))
print(response.data)

print(lat)
print(lon)
print("Bot started...")

data = dict()


def get_id(update):
	return update.message.chat.id


def create_fields(id):
	global data
	data[id] = {'pergunta' : 0, 'src': '', 'dest': '', 'contrycode' : '', 'adults' : '', 'data' : '', 'upsell' : '', 'Permanence' : False}


def start_command(update, context):
	global data
	update.message.reply_text("Seja bem vindo ao seu ajudante virtual. Acredito que você precise de ajuda para iniciar sua jornada como nômade! Digite 'go' para encontrar o voo que te levará a seu próximo destino!")
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
	updater = Updater('5513016229:AAH99XIqBllKTdnV6RNEAKp3_kgAMemfBZI', use_context = True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start_command))
	dp.add_handler(CommandHandler("help", help_command))

	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_error_handler(error)

	updater.start_polling()
	updater.idle()

main()
