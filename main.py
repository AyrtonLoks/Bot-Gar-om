import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

agradecimentos = ["vlw", "obg", "valeu", "obrigado", "vlw, campeão", "obg, campeão"]

resp_agrad = ["nada", "de nada", "não há de que", "é nois!"]

if "respondendo" not in db.keys():
  db["respondendo"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return (quote)

def update_resp_agrad(message):
  if "resp_agrad" in db.keys():
    respostas = db["resp_agrad"]
    respostas.append(message)
    db["resp_agrad"] = respostas
  else:
    db["resp_agrad"] = [message]

def delete_resp_agrad(index):
  respostas = db["resp_agrad"]
  if len(respostas) > index:
    del respostas[index]
    db["resp_agrad"] = respostas

@client.event
async def on_ready():
  print('Tô batendo o meu ponto como {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$lança a braba'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('$campeão'):
    await message.channel.send('Opa!')

  if db["respondendo"]:
    options = resp_agrad
    if "resp_agrad" in db.keys():
      options = options + db["resp_agrad"]
    if any(word in msg for word in agradecimentos):
      await message.channel.send(random.choice(options))

  if msg.startswith("$nova"):
    resposta = msg.split("$nova ",1)[1]
    if not resposta in db["resp_agrad"]:
      update_resp_agrad(resposta)
      await message.channel.send("Adicionei essa nova resposta aos agradecimentos.")
    else:
      await message.channel.send("Essa resposta eu já conheço.")

  if msg.startswith("$del"):
    respostas = []
    if "resp_agrad" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_resp_agrad(index)
      respostas = db["resp_agrad"]
      await message.channel.send("Apaguei essa resposta aos agradecimentos.")
    else:
      await message.channel.send("Desconheço tal resposta.")
    await message.channel.send(respostas)

  if msg.startswith("$lista"):
    lista = []
    if "resp_agrad" in db.keys():
      lista = db["resp_agrad"] + resp_agrad
    await message.channel.send(lista)

  if msg.startswith("$resposta"):
    value = msg.split("$resposta ",1)[1]

    if value.lower() == "true":
      db["respondendo"] = True
      await message.channel.send("OK! Tô aqui, parceiro.")
    elif value.lower() == "false":
      db["respondendo"] = False
      await message.channel.send("Sem respostas então, parceiro.")
    else:
      await message.channel.send("Não entendi o que você quis dizer.")

keep_alive()
client.run(os.getenv('TOKEN'))