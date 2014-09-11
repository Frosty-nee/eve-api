import requests
import xml.etree.ElementTree as ET
from datetime import datetime

api_url = 'https://api.eveonline.com'
# if for some reason you want to access the sisi api server, change this
# to 'https://api.testeveonline.com'
'''
def AccountStatus:
'''
def APIKeyInfo(key_id, key_vcode):
	data = {'keyID': key_id, 'vCode' : key_vcode}
	query = Query('/account/APIKeyInfo.xml.aspx', data)
	query.chars = []
	query.accessmask = query.tree.find('./result/').attrib['accessMask']
	query.type = query.tree.find('./result/').attrib['type']
	try:
		query.expires = datetime.strptime(query.tree.find('./result/').attrib['expires'], '%Y-%m-%d %H:%M:%S')
	except ValueError:
		query.expires = ''
	for char in query.tree.findall('./result/key/rowset/*'):
		query.chars.append(char.attrib)
	return(query)


def Characters(key_id, key_vcode):
	data = {'keyID': key_id, 'vCode': key_vcode}
	query = Query('/account/Characters.xml.aspx', data)
	query.chars = []
	for char in query.characters.rows:
		query.chars.append(char)
	return(query)


def AccountBalance(key_id, key_vcode, charid=None):
	data = {'keyID': key_id, 'vCode': key_vcode, 'characterID': charid}
	query = Query('/char/AccountBalance.xml.aspx', data)
	account =  query.tree.find('./result/rowset/')
	query.accountid = account.attrib['accountID']
	query.accountkey = account.attrib['accountKey']
	query.balance = account.attrib['balance']
	return query
'''
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
'''
def CharacterAffiliation(charids):
	#accepts a tuple of charids and returns an array of dicts containing the requested info
	data = {'ids': charids}
	query = Query('/eve/CharacterAffiliation.xml.aspx', data)
	chars = []
	for c in query.characters.rows:
		chars.append(c)
	return(chars)

def CharacterID(names):
	#returned rows have attribtes 'name' and 'characterid'
	data = {'names': names}
	query = Query('/eve/CharacterID.xml.aspx', data)
	ids = []
	#add each row in the rowset as a dict, then return them
	for name in query.characters.rows:
		ids.append(name)
	return (ids)

def CharacterInfo(charid, key_id=None, key_vcode=None):
	#can be called with no API key, limited, or full
	data = { 'keyID' : key_id, 'vCode' : key_vcode, 'characterID': charid }
	query = Query('/eve/CharacterInfo.xml.aspx', data)
	query.corps = []
	#stick corp history an an array for easier access
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

'''
def EVEFacWarStats():
	query = Query('/eve/FacWarStats.xml.aspx', "")
	query.factionlist = []
	for faction in query.factions.rows:
		query.factionlist.append(faction)
	return(query)

def EVEFacWarTopStats():
	query = Query('/eve/FacWarTopStats.xml.aspx', "")
	#this whole thing makes me sad
	query.playerkillsyesterday = []
	query.playerkillslastweek = []
	query.playerkillstotal = []
	query.playervpyesterday = []
	query.playervplastweek = []
	query.playervptotal = []
	query.corpkillsyesterday = []
	query.corpkillslastweek = []
	query.corpkillstotal = []
	query.corpvpyesterday = []
	query.corpvplastweek = []
	query.corpvptotal = []
	query.factionkillsyesterday = []
	query.factionkillslastweek = []
	query.factionkillstotal = []
	query.factionvpyesterday = []
	query.factionvplastweek = []
	query.factionvptotal = []

	for char in query.characters.KillsYesterday.rows:
		query.playerkillsyesterday.append(char)
	for char in query.characters.KillsLastWeek.rows:
		query.playerkillslastweek.append(char)
	for char in query.characters.KillsTotal.rows:
		query.playerkillstotal.append(char)
	for char in query.characters.VictoryPointsYesterday.rows:
		query.playervpyesterday.append(char)
	for char in query.characters.VictoryPointsLastWeek.rows:
		query.playervplastweek.append(char)
	for char in query.characters.VictoryPointsTotal.rows:
		query.playervptotal.append(char)

	for char in query.characters.KillsYesterday.rows:
		query.corpkillsyesterday.append(char)
	for char in query.characters.KillsLastWeek.rows:
		query.corpkillslastweek.append(char)
	for char in query.characters.KillsTotal.rows:
		query.corpkillstotal.append(char)
	for char in query.characters.VictoryPointsYesterday.rows:
		query.corpvpyesterday.append(char)
	for char in query.characters.VictoryPointsLastWeek.rows:
		query.corpvplastweek.append(char)
	for char in query.characters.VictoryPointsTotal.rows:
		query.corpvptotal.append(char)


	for char in query.characters.KillsYesterday.rows:
		query.factionkillsyesterday.append(char)
	for char in query.characters.KillsLastWeek.rows:
		query.factionkillslastweek.append(char)
	for char in query.characters.KillsTotal.rows:
		query.factionkillstotal.append(char)
	for char in query.characters.VictoryPointsYesterday.rows:
		query.factionvpyesterday.append(char)
	for char in query.characters.VictoryPointsLastWeek.rows:
		query.factionvplastweek.append(char)
	for char in query.characters.VictoryPointsTotal.rows:
		query.factionvptotal.append(char)

	return(query)
'''
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
		try:
			self.key = attributes['key']
		except KeyError:
			self.key = None
		self.rows = []
		for row in rowset.findall('./row'):
			self.rows.append(Row(row))

class List:
	def __init__(self, list):
		pass

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
