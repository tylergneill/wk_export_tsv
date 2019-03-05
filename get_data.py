import requests, json
from collections import OrderedDict
from tqdm import tqdm
import pickle

try: my_api_key = open('api_key.txt','r').read() # either place api_key in little text file
except IOError: my_api_key = "" # or ADD YOUR API KEY HERE

data_store_fn = "data_store.p"
burned_levels_fn = "burned_levels.p"

def save_cornichon(thing, fn):
	f = open(fn, 'w')
	P = pickle.Pickler(f)
	P.dump(thing)
	f.close()
def load_cornichon(fn, thing_type_empty):
	try: f = open(fn, 'r')
	except IOError: return thing_type_empty
	thing = pickle.load(f)
	f.close()
	return thing


class UserSpecific(object):
	def __init__(self, level, meaning, user_specifc_stats):
		self.srs_score = user_specifc_stats['srs_numeric']

	def generate_unique_id(self):
		if self.character != None: self.id = hash(self.type + self.character)
		else: self.id = hash(self.type + self.image_fn)

class Radical(UserSpecific):
	def __init__(self, item_dict):
		self.type = 'radical'
		self.level = item_dict['level']
		self.meaning = item_dict['meaning']
		self.character = item_dict['character']
		if self.character == None: self.image_fn = item_dict['image_file_name']
		UserSpecific.__init__(self, 
			item_dict['level'], item_dict['meaning'], item_dict['user_specific'])
		self.generate_unique_id()

class Kanji(UserSpecific):
	def __init__(self, item_dict):
		self.type = 'kanji'
		self.level = item_dict['level']
		self.meaning = item_dict['meaning']
		self.character = item_dict['character']
		self.onyomi = item_dict['onyomi']
		self.kunyomi = item_dict['kunyomi']
		self.important_reading = item_dict['important_reading']
		UserSpecific.__init__(self, 
			item_dict['level'], item_dict['meaning'], item_dict['user_specific'])
		self.generate_unique_id()

class Vocab(UserSpecific):
	def __init__(self, item_dict):
		self.type = 'vocab'
		self.level = item_dict['level']
		self.meaning = item_dict['meaning']
		self.character = item_dict['character']
		self.kana = item_dict['kana']
		self.pitch = [] # to be populated later
		UserSpecific.__init__(self, 
			item_dict['level'], item_dict['meaning'], item_dict['user_specific'])
		self.generate_unique_id()

Constructors = {
	'radicals': Radical,
	'kanji': Kanji,
	'vocabulary': Vocab,
}


def get_latest():

	global my_api_key

	fetched_item_objects = OrderedDict()

	for type in tqdm(['radicals', 'kanji', 'vocabulary']):

		# fetch new data
		
		url = "https://www.wanikani.com/api/user/%s/%s" % (my_api_key, type)
		response = requests.get(url)
		json_data = json.loads(response.text) # convert to corresponding python dict format
		new_item_data = json_data['requested_information']
		try:
			if 'general' in new_item_data.keys():
				new_item_data = new_item_data['general'] # adjust for vocab peculiarity
		except AttributeError: pass

		# parse new data into objects

		for r_u in new_item_data:
	 		try:
				if r_u['user_specific'] == None: continue
				new_item_object = Constructors[type](r_u)
				fetched_item_objects[new_item_object.id] = new_item_object
	 		except TypeError:
				print "TypeError..."; import pdb; pdb.set_trace()

	return fetched_item_objects