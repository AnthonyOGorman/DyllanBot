import os
import asyncio

import discord
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.vc = None
		
	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			if message.author == self.bot.user: return
			if message.author.bot: return
			if any(word in message.content for word in word_list):
				await message.channel.send('Thats awesome man')
		except Exception as e:
			print('{0}'.format(e))

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if member == self.bot.user: return
		if self.vc is not None and self.vc.is_playing(): return
		if after.channel is not None:
			await self.bot.wait_until_ready()
			try:
				channel = after.channel
				if not self.is_connected(member.guild):
					self.vc = await channel.connect()
				else:
					await self.vc.move_to(channel)
				self.vc.play(discord.FFmpegPCMAudio('src/nerfthis.mp3'))
				while self.vc.is_playing():
					await asyncio.sleep(1)
				await self.vc.disconnect()
			except Exception as e:
				print('{0}'.format(e))

	def is_connected(self, guild):
		vc = discord.utils.get(self.bot.voice_clients, guild=guild)
		return vc and vc.is_connected()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))

word_list = []
with open('src/verbs.txt') as fd:
	text = fd.read()
	word_list = text.splitlines()

bot.add_cog(Events(bot))
my_secret = os.environ['TOKEN']
bot.run(my_secret)