import os
import asyncio
import glob
import secrets
import random
import discord
from discord.ext import commands
from discord.ext.tasks import loop


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.voice_client = None

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

		await self.play_music(secrets.choice(mp3_list), after.channel)


	def get_voice_client(self, guild):
		return discord.utils.get(self.bot.voice_clients, guild=guild)
	
	def reset_voice_client_if_disconnected(self):
		try:
			if self.voice_client and not self.voice_client.is_connected():
				self.voice_client = None
		except Exception as e:
			self.voice_client = None

	async def play_music(self, music, channel):
		# Check if bot was forcably disconnected
		self.reset_voice_client_if_disconnected()

		# If bot already connected to voice client & is playing music, stop.
		if self.voice_client is not None and self.voice_client.is_playing(): 
			self.voice_client.stop()

		# Try connect/move to the channel
		try:
			await self.bot.wait_until_ready()
			if self.voice_client is None:
				self.voice_client = await channel.connect(timeout=5.0)
			elif self.voice_client.channel is not channel:
				await self.voice_client.move_to(channel)

			# Play music
			source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music))
			self.voice_client.play(source, after= lambda e: print('Player error: %s' % e) if e else None)

		except Exception as e:
			print('{0}'.format(e))
			if self.voice_client is not None:
				await self.voice_client.disconnect()
				self.voice_client = None
			return

	@commands.command()
	async def leave(self, ctx):
		await ctx.voice_client.disconnect()
		self.voice_client = None
		await ctx.channel.send('I love egg')
	
	@loop(seconds=60)
	async def random_voice(self):
		if self.voice_client is not None:
			# Random chance to talk around twice an hour
			if random.randrange(0,30)+1 == 30:
				await self.play_music(".\src\sound\stfu.mp3", self.voice_client.channel)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("Egg "))

@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))

if __name__ == '__main__':
	# Load word list
	word_list = []
	with open('src/verbs.txt') as fd:
		text = fd.read()
		word_list = text.splitlines()	

	# Sound (leveled) list
	leveled_list = []
	with open('src/leveled.txt') as fd:
		text = fd.read()
		leveled_list = text.splitlines()	

	# MP3 List
	mp3_list = glob.glob('src/sound/*.mp3')

	# Create bot
	event = Events(bot)

	# Start tasks
	event.random_voice.start()

	bot.add_cog(event)
	my_secret = os.environ['TOKEN']
	bot.run(my_secret)

	