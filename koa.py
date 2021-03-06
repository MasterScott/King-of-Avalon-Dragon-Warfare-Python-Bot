# -*- coding: utf-8 -*-
from crypter import AesCoder
import json
import os
import requests
import random
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class KOA(object):
	def __init__(self,guid):
		print 'using %s as guid'%guid
		self.url='http://koa-global.kingsgroupgames.com/api//'
		self.url_login='https://koa-passport.kingsgroupgames.com/client_api.php'
		self.lang="en"
		self.idfv=self.rndDeviceId()
		self.social_id=""
		self.kingdom_id=0
		self.fpid=None
		self.device_lang="en-GB"
		self.time_zone=""
		self.os_version="0.0.00"
		self.sys_lang="en-GB"
		self.idfa="00000000-0000-0000-0000-000000000000"
		self.device="IPhonePlayer"
		self.app_version="0.0.0"
		self.session_key=None
		self.city_id=None
		self.user_city=None
		self.token=None
		self.uid=None
		self.world_id=None
		self.os="ios"
		self.android_id=""
		self.gaid=""
		self.seq=0
		self.race_mode=0
		self.cv="1571230905"
		self.bvr="6.9.2.912.R"
		self.bvg="6.9.2.912.G"
		self.client_version="6.9.2"
		self.guid=guid
		self.user_info=None
		self.city_map=None
		self.already_init=False
		self.s=requests.session()
		self.s.verify=False
		self.s.headers.update({'X-Unity-Version':'5.5.6f1','Pragma':'no-cache','GDataVer':'v1','Accept':'*/*','Expires':'0','Accept-Encoding':'gzip','Accept-Language':'en-gb','Cache-Control':'no-cache','Content-Type':'application/octet-stream','User-Agent':'kingofavalon/912 CFNetwork/808.2.16 Darwin/16.3.0'})
		self.crypter=AesCoder()
		self.express_signin()

	def rndHex(self,n):
		return ''.join([random.choice('0123456789ABCDEF') for x in range(n)])
	
	def rndDeviceId(self):
		s='%s-%s-%s-%s-%s'%(self.rndHex(8),self.rndHex(4),self.rndHex(4),self.rndHex(4),self.rndHex(12))
		return s

	def express_signin(self):
		d='app_version=6.9.2.912&method=login&l=en-GB&game_id=2031&guid=%s&sdk_version=3.2.75&idfa=00000000-0000-0000-0000-000000000000'%(self.guid)
		auth=self.crypter.MakeSigV3(d)
		data= json.loads(self.s.post(self.url_login,data=d,headers={'Content-Type':'application/x-www-form-urlencoded','User-Agent':'kingofavalon/178 CFNetwork/808.2.16 Darwin/16.3.0','Connection':'keep-alive','Accept-Language':'en-gb','Authorization':auth,'Accept-Encoding':'gzip, deflate'}).content)
		self.fpid=data['data']['fpid']
		self.session_key=data['data']['auth_token']
		self.init()
	
	def buildPOST(self,method,class_,params,commit=False):
		tmp={}
		if commit:
			tmp['race_mode']=self.race_mode
			tmp['seq']=self.seq
			self.seq=self.seq+1
		tmp['params']=params
		tmp['method']=method
		tmp['class']=class_
		tmp['req_id']=str(int(time.time() * 1000))
		return self.sendCMD(json.dumps(tmp))
		
	def sendCMD(self,cmd):
		r=self.s.post(self.url,data=self.crypter.Encode(cmd))
		return json.loads(self.crypter.Decode(r.content,True))

	def init(self):
		data= self.buildPOST(method='init',class_='call',params={"device_lang":self.device_lang,"os":self.os,"cv":self.cv,"fpid":self.fpid,"social_id":"","client_version":self.client_version,"idfa":self.idfa,"time_zone":"+03:00","os_version":self.os_version,"session_key":self.session_key,"idfv":self.idfv,"gaid":"","app_version":"0.0.0","currency_code":"EUR","lang":"en","kingdom_id":0,"sys_lang":"en-GB"})
		self.city_id=data['data']['user_city'][0]['city_id']
		self.user_city=data['data']['user_city'][0]
		self.user_info=data['data']['user_info'][0]
		self.city_map=data['data']['city_map']
		self.uid=data['data']['user_info'][0]['uid']
		self.world_id=data['data']['user_info'][0]['world_id']
		self.token=data['payload']['token']
		self.seq=1

	def getKingdomBuffList(self):
		return self.buildPOST(method='getKingdomBuffList',class_='Wonder',params={"client_version":self.client_version,"token":self.token})

	def getDiyInfo(self):
		return self.buildPOST(method='getDiyInfo',class_='casino',params={"client_version":self.client_version,"token":self.token})

	def getPaymentLevel(self):
		return self.buildPOST(method='getPaymentLevel',class_='Player',params={"token":self.token,"client_version":self.client_version,"uid":self.uid})

	def checkFirstJoinAlliance(self):
		return self.buildPOST(method='checkFirstJoinAlliance',class_='Alliance',params={"client_version":self.client_version,"token":self.token})

	def loadUserBank(self):
		return self.buildPOST(method='loadUserBank',class_='player',params={"token":self.token,"client_version":self.client_version,"uid":self.uid})

	def getIntegralActivityState(self):
		return self.buildPOST(method='getIntegralActivityState',class_='activity',params={"client_version":self.client_version,"token":self.token})

	def enterKingdomBlock(self):
		return self.buildPOST(method='enterKingdomBlock',class_='Map',params={"city_id":self.city_id,"leave":self.leave,"client_version":self.client_version,"token":self.token,"enter":self.enter})

	def getIapPackage(self):
		return self.buildPOST(method='getIapPackage',class_='Player',params={"client_version":self.client_version,"token":self.token})

	def getUnReadCount(self):
		return self.buildPOST(method='getUnReadCount',class_='Mail',params={"client_version":self.client_version,"token":self.token})

	def getBigTimeChest(self):
		return self.buildPOST(method='getBigTimeChest',class_='gift',params={"client_version":self.client_version,"token":self.token})

	def loginCheckSingleActivityState(self):
		return self.buildPOST(method='loginCheckSingleActivityState',class_='activity',params={"client_version":self.client_version,"token":self.token})

	def loadWarList(self):
		return self.buildPOST(method='loadWarList',class_='Alliance',params={"client_version":self.client_version,"token":self.token})

	def paymentPackage(self):
		return self.buildPOST(method='paymentPackage',class_='player',params={"client_version":self.client_version,"token":self.token})

	def getPaymentReturnInfo(self):
		return self.buildPOST(method='getPaymentReturnInfo',class_='PaymentReturn',params={"client_version":self.client_version,"token":self.token})

	def getSuperLoginState(self):
		return self.buildPOST(method='getSuperLoginState',class_='Activity',params={"client_version":self.client_version,"token":self.token})
		
	def commit(self,args,op):
		return self.buildPOST(method='commit',class_='call',params={"bvr":self.bvr,"args":args,"fpid":self.fpid,"token":self.token,"bvg":self.bvg,"client_version":self.client_version,"session_key":self.session_key,"os":self.os,"cv":self.cv,"op":op},commit=True)
		
	def ctime(self):
		return int(time.time())
		
	def freeSpeedup(self,job_id):
		res= self.commit({"job_id": job_id},"City:freeSpeedup")
		time.sleep(1)
		if res['ok']==1:
			print 'building upgraded'
		else:
			print 'problem with upgrade'
		return res
		
	def upgradeObject(self,building_id):
		bdata= self.commit({"city_id": self.city_id, "c_job_id": 0, "building_id": building_id, "instant": False, "gold": 0},"City:upgradeObject")
		return self.freeSpeedup(bdata['data']['set']['job'][0]['job_id'])
			
	def addObject(self,city_id,building_id,slot_id,type):
		bdata= self.commit({"instant": False, "gold": 0, "city_id": city_id, "c_job_id": 0, "slot_id": slot_id, "building_id": building_id, "type": type},"City:addObject")
		return self.freeSpeedup(bdata['data']['set']['job'][0]['job_id'])

	def collectResource(self,building_id):
		return self.commit({"building_ids": [building_id]},"City:collectResource")
			
	def cancelBuild(self,building_id):
		return self.commit({"city_id": self.city_id, "building_id": building_id},"City:cancelBuild")
			
	def getTimerChestInfo(self):
		return self.commit({"uid": self.uid},"Gift:getTimerChestInfo")
			
	def openTimerChest(self):
		return self.commit({"uid": self.uid},"Gift:openTimerChest")
			
	def getList(self,category):
		return self.commit({"category": category, "last_mail_id": 0},"Mail:getList")
			
	def gainAttachment(self,category,mail_id):
		return self.commit({"category": category, "mail_id": mail_id},"Mail:gainAttachment")
			
	def checkCityNameAvailable(self,name):
		return self.commit({"name": name},"City:checkCityNameAvailable")

	def useConsumableItem(self,name):
		return self.commit({"buy": False, "name": name, "city_id": self.city_id, "amount": 1, "item_id": 6000098, "current_world_id": 189, "uid": self.uid},"Item:useConsumableItem")['ok']
			
	def checkMail(self):
		self.getList(0)
		mm= self.getList(3)['payload']['list']
		for m in mm:
			self.gainAttachment(3,m['mail_id'])
			
	def upgradeBuildings(self):
		self.refreshTokens()
		for b in self.city_map:
			#print b['type'],b['level']
			if b['type']==5 or b['type']==7:
				if b['level'] < 3:
					self.upgradeObject(b['building_id'])
				
	def refreshTokens(self):
		self.express_signin()
		self.init()
		
	def completeTutorial(self):
		if self.fpid == None:
			self.express_signin()
		if self.token == None:
			self.init()
		self.getIntegralActivityState()
		self.getIapPackage()
		self.getUnReadCount()
		self.getBigTimeChest()
		self.loginCheckSingleActivityState()
		self.loadWarList()
		self.paymentPackage()
		self.getPaymentReturnInfo()
		self.getSuperLoginState()
		self.getKingdomBuffList()
		self.getDiyInfo()
		self.getPaymentLevel()
		self.checkFirstJoinAlliance()
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX2x1bWJlcl9taWxsLjQifX0="},"Player:setTutorial")
		self.commit({"city_id": self.city_id, "step": 1000, "type": 200032, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX2JhcnJhY2tzLjQifX0="},"Player:setTutorial")
		self.commit({"city_id": self.city_id, "step": 1001, "type": 200187, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX2Zhcm0uNSJ9fQ=="},"Player:setTutorial")
		self.commit({"city_id": self.city_id, "step": 1002, "type": 200001, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX3Ryb29wLjQifX0="},"Player:setTutorial")
		self.commit({"count": 20, "instant": False, "gold": 0, "city_id": self.city_id, "building_id": 1001, "class": "infantry_t1"},"City:trainTroop")
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX3RpcHMuMiJ9fQ=="},"Player:setTutorial")
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIn19"},"Player:setTutorial")
		self.addObject(self.city_id,self.ctime(),36,200001)
		self.commit({"city_id": self.city_id, "quest_id": 400001},"Quest:collectEmpireQuestReward")
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJUdXRvcmlhbF9raW5nZG9tLjUifX0="},"Player:setTutorial")
		#need map support
		#self.commit({"troops": {"ranged_t1": 100, "infantry_t1": 100, "cavalry_t1": 100}, "city_id": self.city_id, "k": 189, "with_dragon": 0, "y": 2492, "x": 478, "type": "gather", "job_id": "6386186911106334722"},"PVP:startMarch")
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJmaW5pc2hlZCJ9fQ=="},"Player:setTutorial")
		self.upgradeObject(1)
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJmaW5pc2hlZCIsIlR1dG9yaWFsX21pbGl0YXJ5X3RlbnQiOiJmaW5pc2hlZCJ9fQ=="},"Player:setTutorial")
		self.commit({"city_id": self.city_id, "quest_id": 400002},"Quest:collectEmpireQuestReward")
		self.commit({"uid": self.uid, "level": 2},"Hero:notifyLastLevel")
		self.addObject(self.city_id,self.ctime(),33,200032)
		self.addObject(self.city_id,self.ctime(),34,200032)
		self.addObject(self.city_id,self.ctime(),37,200032)
		self.addObject(self.city_id,self.ctime(),38,200001)
		self.addObject(self.city_id,self.ctime(),42,200001)
		self.addObject(self.city_id,self.ctime(),40,200590)
		self.commit({"city_id": self.city_id, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJmaW5pc2hlZCIsIlR1dG9yaWFsX21pbGl0YXJ5X3RlbnQiOiJmaW5pc2hlZCIsIlR1dG9yaWFsX21haWwiOiJmaW5pc2hlZCJ9fQ=="},"Player:setTutorial")
		self.addObject(self.city_id,self.ctime(),39,200590)
		print 'tutorial completed'