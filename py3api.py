import requests
import xml.etree.ElementTree as ET
from datetime import datetime

api_url = 'https://api.eveonline.com'
# if for some reason you want to access the sisi api server, change this
# to 'https://api.testeveonline.com'
'''
def AccountStatus:

def APIKeyInfo:

def Characters:

def AccountBalance:

def AssetList:

def Blueprints:

def CalendarEventAttendees:
'''
def CharacterSheet(key_id, key_code, key_mask, character_id):
	allowed(key_mask, 8)
	data = {'keyID': key_id, 'vCode': key_code, 'characterID': character_id}
	query = Query('/char/CharacterSheet.xml.aspx', data)

	# Fix up the data a bit
	query.birthday = datetime.strptime(query.dob, '%Y-%m-%d %H:%M:%S')
	query.bio = ' - '.join([query.gender, query.race, query.bloodline, query.anscestry])
	query.memory = query.attributes.memory
	query.intelligence = query.attributes.intelligence
	query.perception = query.attributes.perception
	query.charisma = query.attributes.charisma
	query.willpower = query.attributes.willpower

	try:
		query.memorybonus = query.attributeenhancers.memorybonus.augmentatorvalue
	except AttributeError:
		query.memorybonus = 0
	try:
		query.intelligencebonus = query.attributeenhancers.intelligencebonus.augmentatorvalue
	except AttributeError:
		query.intelligencebonus = 0
	try:
		query.perceptionbonus = query.attributeenhancers.perceptionbonus.augmentatorvalue
	except AttributeError:
		query.perceptionbonus = 0
	try:
		query.charismabonus = query.attributeenhancers.charismabonus.augmentatorvalue
	except AttributeError:
		query.charismabonus = 0
	try:
		query.willpowerbonus = query.attributeenhancers.willpowerbonus.augmentatorvalue
	except AttributeError:
		query.willpowerbonus = 0

	return(query)

'''
def ContactList:

def ContactNotifications:

def ContractBids:

def ContractItems:

def Contracts:

def FacWarStats:

def IndustryJobs:

def KillLog:

def KillMails:

def Locations:

def MailBodies:

def MailingLists:

def MailMessages:

def Medals:

def Notifications:

def NotificationTexts:

def PlanetaryColonies:

def PlanetaryLinks:

def PlanetaryPins:

def PlanetaryRoutes:

def Research:

def SkillInTraining:

def SkillQueue:

def Standings:

def UpcomingCalendarEvents:

def WalletJournal:

def WalletTransactions:

def CorpAccountBalance:

def CorpAssetList:

def CorpContactList:

def CorpContainerLog:

def CorpContractBids:

def CorpContractItems:

def CorpContracts:

def CorpCorporationSheet:

def CorpFacilities:

def CorpFacWarStats:

def CorpKillLog:

def CorpKillMails:

def CorpLocations:

def CorpMarketOrders:

def CorpMedals:

def CorpMemberMedals:

def CorpMemberSecurity:

def CorpMemberSecurityLog:

def CorpMemberTracking:

def CorpOutpostList:

def CorpOutpostServiceDetail:

def CorpSharholders:

def CorpStandings:

def CorpStarbaseDetail:

def CorpStarbaseList:

def CorpTitles:

def CorpWalletJournal:

def CorpWalletTransactions:

def AllianceList:

def CertificateTree:

def CharacterAffiliation:
'''
def CharacterID(names):
	#returned rows have attribtes 'name' and 'characterid'
	data = {'names': names}
	query = Query('/eve/CharacterID.xml.aspx', data)
	ids = []
	#add each row in the rowset as a dict, then return them
	for name in query.characters.rows:
		ids.append(name)
	return (ids)

def CharacterInfo(key_id, key_vcode, charid):
	#can be called with no API key, limited, or full
	data = { 'keyID' : key_id, 'vCode' : key_vcode, 'characterID': charid }
	query = Query('/eve/CharacterInfo.xml.aspx', data)
	query.corps = []
	for corp in query.employmentHistory.rows:
		query.corps.append(corp)
	return (query)

def CharacterName(ids):
	#returned rows have attributes 'name' and 'characterid'
	data = {'ids' : ids}
	query = Query('/eve/CharacterName.xml.aspx', data)
	names = []
	#add each row to the rowset as a dict, then return them
	for id in query.characters.rows:
		names.append(id)
	return(names)

'''
def ConquerableStationList:

def ErrorList:

def EVEFacWarStats:

def EVEFacWarTopStats:

def RefTypes:

def SkillTree:

def TypeName:

def MapFacWarSystems:

def Jumps:

def Kills:

def Sovereignty:

def SovereigntyStatus:

def ServerStatus:
'''

class Query:
	#full queries turn all child elements of the <result> into attributes
	#which is useful for the character sheet
	def __init__(self,relative_url, data):
		result = requests.post(api_url + relative_url, data)
		if result.status_code == 200:
			self.tree = ET.fromstring(result.text)
			for element in self.tree.findall('./result/*'):
				node = Node(element)
				setattr(self, node.name, node.value)
			cached = self.tree.find('./cachedUntil').text
			self.cached_until = datetime.strptime(cached, '%Y-%m-%d %H:%M:%S')
		elif 400 <= result.status_code < 500:
			print(result.text)
			self.tree = ET.fromstring(result.text)
			message = self.tree.find('error').text
			raise APIException("API Errorr: " + message)

class Rowset:
	def __init__(self, rowset):
		attributes = rowset.attrib
		self.name= attributes['name']
		self.key = attributes['key']
		self.rows = []
		for row in rowset.findall('./row'):
			self.rows.append(Row(row))

class Row:
	def __init__(self, row):
		for k,v in row.attrib.items():
			setattr(self, k.lower(), v)

	def __str__(self):
		return("<Row: " + str(self.__dict__) + ">")

class Node:
	def __init__(self, element):
		if element.tag.lower() == 'rowset':
			rowset = Rowset(element)
			self.name = rowset.name
			self.value = rowset
			return
		self.name = element.tag.lower()
		self.value = element.text
		for child in element:
			node = Node(child)
			setattr(self, node.name, node.value)
			self.value = self

class HttpException(Exception):
	def __init__(self, message):
		self.message = message

class APIException(Exception):
	def __init__(self, message):
		self.message = message
