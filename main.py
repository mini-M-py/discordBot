import os

import discord

import requests
import json
import random

from keep_alive import keep_alive
from gemini import gemini
import time

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
responding = True




sad_words = [
    "sad", "depressed", "unhappy", "angry", "gloomy", "miserable", "downcast",
    "despondent", "melancholy", "despair", "lugubrious", "morose", "forlorn",
    "dismal", "blue", "woeful", "wretched", "sorrowful", "dejected", "glum",
    "gloomy", "sullen", "dreary", "doleful", "crestfallen", "heartbroken",
    "disheartened", "downhearted", "heavyhearted", "mournful", "woebegone",
    "down in the dumps", "cast down", "in the doldrums", "low-spirited",
    "sad-faced", "long-faced", "tearful", "weepy", "melancholic", "plaintive",
    "pensive", "disconsolate", "wistful", "inconsolable", "angst", "regretful",
    "repentant", "remorseful", "shamefaced", "sorry", "penitent", "contrite",
    "guilty", "tortured", "ashamed", "abashed", "chagrined", "mortified",
    "humiliated", "embarrassed", "shy", "sheepish", "apologetic", "clumsy",
    "self-conscious", "red-faced", "blushing", "flushed", "nervous", "edgy",
    "restless", "agitated", "anxious", "apprehensive", "tense", "nervy",
    "jittery", "on edge", "jumpy", "uptight", "twitchy", "neurotic",
    "high-strung", "restive", "overwrought", "wound"
    "up", "keyed up", "uneasy", "uncomfortable", "insecure", "fearful",
    "frightened", "scared", "panicky", "hysterical"
]

encouraging_messages = [
    "You've got this!", "Keep going, you're making progress!",
    "Believe in yourself, you can do it!",
    "You are capable of amazing things.", "Your hard work will pay off.",
    "Stay positive and keep moving forward.",
    "You're stronger than you think.",
    "You've overcome challenges before, and you can do it again.",
    "Every step you take brings you closer to your goals.",
    "Don't give up, you're closer than you think."
]

rules = """\n\nPlease read the rules.\n
1 Be respectful to others.
2 No hate speech, harassment or bullying will be tolerated.
3 No spamming.
4 Use appropriate language and avoid offensive content
5 Do not engage in any form of discrimination.
6 Keep conversation civil and constructive.
7 Have fun and enjoy your the community!"""


def update_encouragements(encouraging_message):
    encouraging_messages.append(encouraging_message)
def delete_encouragement(index):
    encouraging_messages.pop(index)
  
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)

  quote = json_data[0]['q'] + " -" + json_data[0]['a']

  return (quote)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in message.content for word in sad_words):
      options = encouraging_messages
      await message.channel.send(random.choice(options))

  if message.content.startswith('$new'):
    encouraging_message = message.content.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if message.content.startswith('$del'):
      index = int(message.content.split("$del", 1)[1])
      delete_encouragement(index)
      await message.channel.send('deleted')

  if message.content.startswith('$list'):
       await message.channel.send(encouraging_messages)

  if message.content.startswith('$responding'):
    value = message.content.split("$responding ", 1)[1]

    if value.lower() == "true":
      responding = True
      await message.channel.send("Responding is on ")
    else:
      responding = False
      await message.channel.send("Responding is off")

  if message.content.startswith('?'):
    question = message.content.split("?", 1)[1]

    try:
       answer = gemini(question +  "(you are discord bot reply on few word)")
       await message.channel.send(answer )
    except:
      await message.channel.send("I am busy. Please wait for few seconds")
      time.sleep(10)
      answer = gemini(question + "(you are discord bot reply on few word)")
      await message.channel.send(answer)
          
  
   

  if message.content.startswith('$rules'):
    await message.channel.send(rules)

  if message.content.startswith('$help'):
    help_message = "Available commands:\n"
    help_message += "$hello : Say hello\n"
    help_message += "$quote : Get an inspirational quote\n"
    help_message += "$new [message] : Add a new encouraging message\n"
    help_message += "$del [index] : Delete an encouraging message by index\n"
    help_message += "$list : List all encouraging messages\n"
    help_message += "$responding [true/false] : Toggle responding to sad words\n"
    help_message += "? [question] : Ask a question to the AI\n"
    help_message += "$rules : Display the server rules\n"
    await message.channel.send(help_message)


@client.event
async def on_member_join(member):
  guild = member.guild
  channel = discord.utils.get(guild.channels, id=int(os.environ['WELCOME_ID']))
  if channel:
    await channel.send(f'Welcome {member.mention}!' + rules)
  else:
    print('Channel not found')


keep_alive()

client.run(os.environ['BOT_TOKEN'])


