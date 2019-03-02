import requests, json
from collections import OrderedDict
from tqdm import tqdm
import pickle

my_api_key = ""

all_items_fn = "data_store.p"
learning_level_fn = "learning_level.p"		# GET RID OF
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

def get_from_wanikani(simple_type='kanji', level=''):
	global my_api_key
	# defaults to all levels
	# CHANGE TO DOING ONLY ALL LEVELS
	simple_type_to_api_type = {
		'radical': 'radicals', 'kanji': 'kanji', 'vocab': 'vocabulary'
	}
	url = "https://www.wanikani.com/api/user/%s/%s/%s" % (
		my_api_key, simple_type_to_api_type[simple_type], level)
	response = requests.get(url)
	json_data = json.loads(response.text) # convert to corresponding python dict format
	return json_data

class UserSpecific(object):
	def __init__(self, level, meaning, user_specifc_stats):
		self.srs_score = user_specifc_stats['srs_numeric']
# 		self.meaning_correct = user_specifc_stats['reading_correct']
# 		self.meaning_incorrect = user_specifc_stats['reading_incorrect']
# 		self.reading_correct = user_specifc_stats['meaning_correct']
# 		self.reading_incorrect = user_specifc_stats['meaning_incorrect']

	# SHOULDN'T BE NECESSARY ONCE ISOLATING TYPES
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
		self.pitch_pattern = [] # to be populated later
		UserSpecific.__init__(self, 
			item_dict['level'], item_dict['meaning'], item_dict['user_specific'])
		self.generate_unique_id()

Constructors = {
	'radical': Radical,
	'kanji': Kanji,
	'vocab': Vocab,
}

def pull_progress(working_levels):
	pulled_item_objects = OrderedDict()

	# ADJUST FOR NEW DEFAULT: JUST PULL ALL LEVELS OF GIVEN TYPE IN ONE CALL

	for level in working_levels:
		for type in tqdm(['radical', 'kanji', 'vocab'], desc='level %d'%level):
	 		json_data = get_from_wanikani(type, level) # actual website pull
# 			json_data = level_1_example_data[type] # local testing
			try:
				requested_items = json_data['requested_information']
				for r_u in requested_items:
					if r_u['user_specific'] == None: continue
					new_item_object = Constructors[type](r_u)
					pulled_item_objects[new_item_object.id] = new_item_object
			except:
				print "failed to get info for level %d, type '%s'" % (level, type)
				pass
	return pulled_item_objects

# from level_1_example_data import *

# SHOULDN'T NEED ANY MORE
def same_item(u1, u2):
	if (u1.level != u2.level or 
		u1.type != u2.type or 
		u1.character != u2.character or 
		u1.character == u2.character == 'None' and u1.image_fn != u2.image_fn
		): return False
	else: return True

# SHOULDN'T NEED ANY MORE
def consolidate_objects(base={}, additions={}):
	# order of arguments matters
	for new_obj_id in additions.keys():
		base[new_obj_id] = additions[new_obj_id]
	return base
# 
# 	# 'min_index' for optimization: don't waste time looking at lower levels
# 	lowest_level_change = min( [u.level for u in new_item_objects] )
# 	min_index = 0
# 	while base_list_item_objects[min_index].level < lowest_level_change: min_index += 1
# 
# 	for new_u_o in new_item_objects:
# 		for b_l_u_o in base_list_item_objects[min_index:]:
# 			if same_item(b_l_u_o, new_u_o):
# 				base_list_item_objects.remove(b_l_u_o)
# 				base_list_item_objects.append(new_u_o)
# 				break
# 		else: base_list_item_objects.append(new_u_o)
# 
# 	return base_list_item_objects
