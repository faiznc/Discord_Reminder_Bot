import discord
import os
# import requests
# import json
# import random
# from replit import db
from keep_alive import keep_alive
from my_timer import start_timer

client = discord.Client()

token = os.environ['TOKEN']

# def basic_handle_message(command,text):
#   command.lower()
#   print(command)
#   await message.channel.send(parsed)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    msg = message.content
    if message.content.startswith("!"): # idk but it doesnt work
      parsed = message.content[1:]
      parsed = parsed.lower()
      print(parsed)

      #command list here...
      if parsed.startswith("test"):
        await message.channel.send("Test berhasil.")

      if parsed.startswith("set-timer"):
          # harusnya !set-timer 13.50
          parsed = message.content[1:]
          parsed = parsed.lower()
          hh, mm = parsed[10:12], parsed[13:15]
          response = "Timer set to {}:{}".format(hh, mm)
          print(response)
          await message.channel.send(response)

      #set time object to print 

    if msg.startswith("!hello"):  #Default form
        await message.channel.send("Hello to you my friend.")


keep_alive()
print("Starting...")
start_timer()
client.run(token)
