#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json
from collections import OrderedDict
from tqdm import tqdm
import pickle
import ast

try: my_api_key_v1 = open('api_key_v1.txt','r').read() # either place v1 API key in little text file
except IOError: my_api_key_v1 = "" # or ADD YOUR v1 API KEY HERE

# may be updated for v2 later

data_store_fn = "data_store.p"
burned_levels_fn = "burned_levels.p"
pitch_patterns_fn = "pitches.txt"

lines = open(pitch_patterns_fn,'r').read().split('\n')
pitch_table = {}
for l in lines:
	word, pattern = l.split(':')
	pitch_table[word] = ast.literal_eval(pattern)

moraic_kana = [
# hiragana
'あ',	'い',	'う',	'え',	'お',	
'か',	'き',	'く',	'け',	'こ',	
'が',	'ぎ',	'ぐ',	'げ',	'ご',	
'さ',	'し',	'す',	'せ',	'そ',	
'ざ',	'じ',	'ず',	'ぜ',	'ぞ',	
'た',	'ち',	'つ',	'て',	'と',	
'だ',	'ぢ',	'づ',	'で',	'ど',	
'な',	'に',	'ぬ',	'ね',	'の',	
'は',	'ひ',	'ふ',	'へ',	'ほ',	
'ば',	'び',	'ぶ',	'べ',	'ぼ',	
'ぱ',	'ぴ',	'ぷ',	'ぺ',	'ぽ',	
'ま',	'み',	'む',	'め',	'も',	
'や',			'ゆ',			'よ',	
'ら',	'り',	'る',	'れ',	'ろ',	
'わ',	'ゐ',	'ゑ',	'を',	
				'ん',
				'っ',
# katakana
'ア',	'イ',	'ウ',	'エ',	'オ',	
'カ',	'キ',	'ク',	'ケ',	'コ',	
'ガ',	'ギ',	'グ',	'ゲ',	'ゴ',	
'サ',	'シ',	'ス',	'セ',	'ソ',	
'ザ',	'ジ',	'ズ',	'ゼ',	'ゾ',	
'タ',	'チ',	'ツ',	'テ',	'ト',	
'ダ',	'ヂ',	'ヅ',	'デ',	'ド',	
'ナ',	'ニ',	'ヌ',	'ネ',	'ノ',	
'ハ',	'ヒ',	'フ',	'ヘ',	'ホ',	
'バ',	'ビ',	'ブ',	'ベ',	'ボ',	
'パ',	'ピ',	'プ',	'ペ',	'ポ',	
'マ',	'ミ',	'ム',	'メ',	'モ',	
'ヤ',			'ユ',			'ヨ',	
'ラ',	'リ',	'ル',	'レ',	'ロ',	
'ワ',	'ヰ',	'ヱ',	'ヲ',	
				'ン',
				'ッ',
]

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
		self.kana = item_dict['kana'].split(',')[0]
		UserSpecific.__init__(self, 
			item_dict['level'], item_dict['meaning'], item_dict['user_specific'])
		self.generate_unique_id()
		self.count_morae()
		self.lookup_pitch()

	def lookup_pitch(self):
		try: self.pitch = pitch_table[self.character.encode('utf-8')]
		except KeyError:
			self.pitch = [-1]
			print "not found in pitch table: %s    %s" % (self.character, self.kana)

	def count_morae(self):
# 		import pdb;pdb.set_trace()
# 		decoded_kana = .decode('utf-8')  # NECESSARY?
		self.morae = 0
		for kana in self.kana:
			if kana.encode('utf-8') in moraic_kana: self.morae += 1


Constructors = {
	'radicals': Radical,
	'kanji': Kanji,
	'vocabulary': Vocab,
}


def get_latest():

	global my_api_key_v1

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