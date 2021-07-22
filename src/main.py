import os
import asyncio
import glob
import secrets

import discord
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			# Make sure author is not a bot
			if message.author is self.bot.user: return
			if message.author.bot: return
			# Search word list to reply to
			if any(word in message.content for word in word_list):
				await message.channel.send('Thats awesome man')
		except Exception as e:
			print('{0}'.format(e))

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		# Make sure the member is joining a channel
		if after.channel is None: return
		# Make sure member has not moved to AFK
		if after.afk: return
		# Ignore mute / deaf etc.
		if before.channel is after.channel: return
		# Make sure member is not a bot or itself
		if member is self.bot.user: return
		if member.bot: return

		# If bot already connected to voice client & is playing music, stop.
		voice_client = self.get_voice_client(member.guild)
		if voice_client is not None and voice_client.is_playing(): 
			voice_client.stop()

		# Try connect/move to the channel
		try:
			await self.bot.wait_until_ready()
			channel = after.channel
			if voice_client is None:
				voice_client = await channel.connect(timeout=5.0)
			elif voice_client.channel is not channel:
				await voice_client.move_to(channel)

			# Play music
			source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(secrets.choice(mp3_list)))
			voice_client.play(source, after= lambda e: print('Player error: %s' % e) if e else None)

			# Wait while playing
			while voice_client.is_playing():
				await asyncio.sleep(1)

			# Once finished disconnect
			await voice_client.disconnect()
		except Exception as e:
			print('{0}'.format(e))


	def get_voice_client(self, guild):
		return discord.utils.get(self.bot.voice_clients, guild=guild)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))

if __name__ == '__main__':
	# Load word list
	word_list = []
	with open('src/verbs.txt') as fd:
		text = fd.read()
		word_list = text.splitlines()	

	# MP3 List
	mp3_list = glob.glob('src/sound/*.mp3')

	# Create bot
	bot.add_cog(Events(bot))
	my_secret = os.environ['TOKEN']
	bot.run(my_secret)	