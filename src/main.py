import os
import discord

my_secret = os.environ['TOKEN']
word_list = []
with open('verbs.txt') as fd:
	text = fd.read()
	word_list = text.splitlines()

client = discord.Client()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	try:
		if message.author == client.user:
			return

		if any(word in message.content for word in word_list):
			await message.channel.send('Thats awesome man')
	except:
		print('Error')


client.run(my_secret)
