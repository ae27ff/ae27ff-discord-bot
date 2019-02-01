import threading
import json
import urllib.request
import urllib.parse

class AeAPI:
	url = "http://ae27ff.localhost/api/"
	appname = 'Unknown-PyAeAPI-App'
	appid = ''
	appver = '1.0'
	apiver='1.0'

	@classmethod	
	def query_preparedata(cls,data_fields):
		if data_fields is None:
			return None
		json_fields = {k: json.dumps(v) for k,v in data_fields.items()}
		return urllib.parse.urlencode(json_fields).encode('utf-8');

	@classmethod
	def query(cls,qname,fields={},data_fields={}):
		result = {}
		try:
			fields['query']=qname
			fields['appid']=cls.appid
			arguments = urllib.parse.urlencode(fields)
			qurl = cls.url + "?"+ arguments
			req = urllib.request.Request(
				qurl,
				data=cls.query_preparedata(data_fields),
				headers={
					'User-Agent':'PyAeAPI/'+cls.apiver+' '+cls.appname+'/'+cls.appver,
					"Content-Type": "application/x-www-form-urlencoded"
				}
			)
			result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
		except Exception as e:
			result={'neterror':True,'error':e}
		else:
			result['neterror']=False;
		return result

	@classmethod
	def usersonrank(cls,rank):
		return cls.query('usersonrank',{'rank':rank})

	@classmethod
	def progressions(cls,user='*',limit=100):
		return cls.query('progressions',{'user':user,'limit':limit})

	@classmethod
	def lastrankup(cls):
		return cls.query('lastrankup')

	@classmethod
	def userrank(cls,user):
		return cls.query('userrank',{'user':user})

	@classmethod
	def bulkrank(cls,users):
		return cls.query('bulkrank',{},{'users':users});	

	@classmethod
	def activity(cls,days=None):
		if days is None:
			return cls.query('activity')
		return cls.query('activity',{'days':days})

#	timer_func = None	
#	def timershim():
#		if AeAPI.timer_func is not None:
#			print('run timer')
#			AeAPI.timer_func()
#			threading.Timer(60, AeAPI.timershim).start()
#
#
#	def timer(timerfunc):
#		print('set timer func')
#		AeAPI.timer_func = timerfunc		
#		AeAPI.timershim()


