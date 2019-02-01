import discord
import asyncio
import json
import configparser

from AeAPI import * 
from AeRankings import *
from DiscordPins import *

config = configparser.ConfigParser()
client = discord.Client()
clientkey = None
description = '''Placeholder commands description'''

def getconfig(section,key,default):
	if not config.has_option(section,key):
		return default
	return config.get(section,key)	

def load():
	global client
	global clientkey
	config.read('config.cfg')
	AeAPI.appid = getconfig('ae27ff','appid','ae27ff-example-app-id-000-0000-000000000000')
	AeAPI.appname = getconfig('ae27ff','appname','ae-Bot')
	AeAPI.appver = getconfig('ae27ff','appver','0.1')
	clientkey = getconfig('discord','privkey','NO-PRIVKEY-SPECIFIED')
	AeRankings.load()
	DiscordPins.load(client)

def save():
	DiscordPins.save()
	AeRankings.save()

def start():
	client.loop.create_task(my_background_task())
	client.run(clientkey)

def stop():
	save()





##########################################################################

def get_activity_string():
	gstatus='error'
	try:
		gstatus = "ae27ff - "+str(AeAPI.activity()['active'])+" users. "+str(AeAPI.activity(1)['active'])+" on today."
		print(gstatus)
	except Exception as e:
		print(e)
		print(AeAPI.activity())
		print(AeAPI.activity(1))
	return gstatus


def link(text,uri=""):
	return "["+text+"](https://ae27ff.meme.tips"+uri+")"

def field(level,users):
	f = {}
	userlinks = "";
	for user in users:
		userlinks+=link(user,"/u/"+user)+" "
	f['name'] = "__**Level "+str(level)+"**__";
	f['value'] = userlinks
	f['inline']=False
	return f

def userstofields():
	fields = []
	for rank in range(100,0,-1):
		users = [u for (u,r) in AeRankings.rankings.items() if r == rank]
		if len(users)>0:
			fields.append(field(rank,users))
	return fields


async def my_background_task():
	prefix="!ae"
	preEmbedMessage = '**Add your name to the rankings!** \nJust use the command: ```http\n'+prefix+'adduser YourAE27FFName```\n\n**Solved a new level and want to show your progress on the rankings?** \nJust use the command: ```http\n'+prefix+'update```\n\nFor bot managing commands (only for moderators) use: ```http\n'+prefix+'modHelp```';

#	embed = discord.Embed(
#		title="***AE27FF RANKINGS***",
#		type="rich",
#		description="List of member's current levels on ",
#		colour=11413503,


	embed = discord.Embed(**{
		"title": "**AE27FF RANKINGS**",
  		"description": "Member levels on " + link("ae27ff"),
		"color": 11413503,
	});

	embed.set_footer(**{
		"icon_url": "https://cdn.discordapp.com/avatars/431930297328730114/da26cbbc0f89134763b03396783a96cb.png",
		"text": "Bot inspired by Luis"
	});



	await client.wait_until_ready()
	while not client.is_closed:
		AeRankings.save()
		DiscordPins.save()
		AeRankings.update()
		embed.clear_fields()
		for field in userstofields():
			embed.add_field(**field)
		await DiscordPins.editall(preEmbedMessage,embed)
		await client.change_presence(game=discord.Game(name=get_activity_string()))
		await asyncio.sleep(60) # task runs every 60 seconds



@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	AeRankings.adduser("crashdemons")
	AeRankings.adduser("amone")
	AeRankings.update()
	print(AeRankings.rankings)
	await client.change_presence(game=discord.Game(name='ae27ff'))

@client.event
async def on_message(message):
	if message.content.startswith('!aecreate'):
		tmp = await DiscordPins.create(message.channel,"Loading content...")
	elif message.content.startswith('!aedelete'):
		result = await DiscordPins.remove(message.channel)
		if result:
			await client.send_message(message.channel,"Channel message deleted.")
		else:
			await client.send_message(message.channel,"Channel message not found.")
	elif message.content.startswith('!aeadduser'):
		param = message.content[len('!aeadduser '):]
		if len(param)>0:
			AeRankings.adduser(param)
			await client.send_message(message.channel,"Added "+str(param)+" to rankings")
		else:
			await client.send_message(message.channel,"Which user?")
			

#this is standard, but the example command is never fired (when using client = commands.Bot(...)), so the discord.ext syntax seems useless(?)
#@bot.command()
#async def aeadduser(user: str):
#	AeRankings.adduser(user)
#	await bot.say("Added user "+str(user)+" to rankings.")





######################################################################

load()
start()
