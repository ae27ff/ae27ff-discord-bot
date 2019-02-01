import discord
import json

class DiscordPins:
	filename = "pins.json"
	client = None
	pins = {}

	@classmethod
	def load(cls,client):
		cls.client = client
		try:
			cls.pins = json.load(open(cls.filename))
		except FileNotFoundError:
			print("Pins file not initialized.");

	@classmethod
	def save(cls):
                json.dump(cls.pins, open(cls.filename, 'w'))

	@classmethod
	def getmidfromcid(cls, channelid):
		try:
			return cls.pins[channelid]
		except KeyError:
			return None

	@classmethod
	def addid(cls,channelid,messageid):
		cls.pins[channelid]=messageid
		#cls.pins.append( {"channel":channelid, "message":messageid} );

	@classmethod
	async def getfromid(cls,channelid,messageid=None):
		if messageid == None:
			messageid = cls.getmidfromcid(channelid)
		if messageid == None:
			return None
		try:
			channel = cls.client.get_channel(channelid)
			if channel == None:
				print("couldn't find channel "+str(channelid))
				return None
			return await cls.client.get_message(channel, messageid)
		except discord.NotFound:
			return None

	@classmethod
	async def removeid(cls,channelid):
		message = await cls.getfromid(channelid)
		if message == None:
			return False 
		await cls.client.delete_message(message)
		cls.pins.pop(channelid,None)
		return True	

	@classmethod
	async def remove(cls,channel):
		return await cls.removeid(channel.id)			

	@classmethod
	def add(cls,message):
		cls.addid(message.channel.id,message.id)

	@classmethod
	async def editall(cls,new_content=None,embed=None):
		keys = list(cls.pins.keys())
		for channelid in keys:
			print("edit message for channel: " + channelid)
			message = await cls.getfromid(channelid)
			print("   message found: "+str(message))
			if message == None:
				cls.pins.pop(channelid,None)
				continue
			await cls.client.edit_message(message, new_content, embed=embed)

	@classmethod
	async def create(cls,channel,content=None,embed=None):
		message = await cls.client.send_message(channel,content,embed=embed)
		cls.add(message)
		return message
	
