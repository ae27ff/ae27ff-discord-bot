import json

from AeAPI import *

class AeRankings:
	filename = "rankings.json"
	rankings = {}
	updated = False	

	@classmethod
	def load(cls):
		try:
			cls.rankings = json.load(open(cls.filename))
		except FileNotFoundError:
			print("Rankings file not initialized.");

	@classmethod
	def save(cls):
		json.dump(cls.rankings, open(cls.filename, 'w'))

	@classmethod
	def update(cls):
		users = list(cls.rankings.keys())
		result = AeAPI.bulkrank(users)
		entries = result['users']
		for entry in entries:
			cls.rankings[entry['user']] = entry['rank']
		cls.updated = True

	@classmethod
	def adduser(cls,user):
		cls.rankings[user]=-1 # add user regardless of API exception
		result = AeAPI.userrank(user)
		#print("userrank dump: ")
		#print(result)
		cls.rankings[user]=result['rank']
		cls.updated = True
