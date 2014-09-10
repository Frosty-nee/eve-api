import requests
import xml.etree.ElementTree as ET
from datetime import datetime

api_url = 'https://api.eveonline.com'
# if for some reason you want to access the sisi api server, change this
# to 'https://api.testeveonline.com'

class Query:
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
