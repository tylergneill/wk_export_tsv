import get_data
from collections import OrderedDict
import sys

choice = ''
try:
	if sys.argv[1] == '-Y': choice = 'Y'
except: pass

def output_tsv(all_item_objects, score_range=(1,9)):
	"""
		Creates customized multi-column tsvs for radicals, kanji, and vocab.
		Can be modified to create flashcards for:
			character-meaning,
			character-important_reading (kanji only),
			character-kana (vocab only), 
			etc. etc.
	"""
	types = ['radical', 'kanji', 'vocab']
	for type in types:
		tsv_fn = type + ".tsv"
		out_f = open(tsv_fn, 'w')
		for score in range(score_range[0],score_range[1]+1):
			out_str = "srs_score %d\n" % score
			out_f.write(out_str.encode('utf-8'))
			for u in all_item_objects.values():
				if u.type != type or u.srs_score != score: continue
				if type == 'radical':
					if u.character == None: rad_character = '_'
					else: rad_character = u.character
					out_str = str(u.level) + '\t' + rad_character + '\t' + u.meaning + '\n'
				elif type == 'kanji':
					out_str = str(u.level) + '\t' + u.character + '\t' + u.meaning + '\n'
				elif type == 'vocab':
# 					out_str = str(u.level) + '\t' + u.character + '\t' + u.meaning + '\n'
					out_str = str(u.level) + '\t' + u.character + '\t' + u.kana + '\t' + str(u.morae) + '\t' + repr(u.pitch) + '\t' + u.meaning + '\n'
				out_f.write(out_str.encode('utf-8'))
		out_f.close()

# initialize with level details

prev_kanji_burned_levels = get_data.load_cornichon(get_data.burned_levels_fn, list())

# get data, either via api or from local storage

if choice != 'Y': choice = raw_input('refresh data? (Y/n)')

if choice == 'Y': # get new item object data and save
	all_item_objects = get_data.get_latest()
	get_data.save_cornichon(all_item_objects, get_data.data_store_fn)

else: # load local item object data
	print "loading previous item data..."
	all_item_objects = get_data.load_cornichon(get_data.data_store_fn, OrderedDict())
	if all_item_objects == OrderedDict(): print "nothing loaded"
	else: print "loaded"

# output object info to tsv files
score_range = (1,9) 	# (1,9) all; (5,6) guru, etc.
output_tsv(all_item_objects, score_range=score_range) 
print "tsv files updated"

### END MAIN PROGRAM



### EXTRA STUFF: determine some level stats

def format_levels(levels):
	"""
		Takes list of level numbers and formats nicely like 1-4, 5, 6-7, etc.
	"""
	if levels == []: return None
	# list assumed to be sorted, non-redundant integers
	all_runs = []; curr_run = [levels[0], levels[0]]
	for curr_level in levels[1:]:
		if curr_level == curr_run[1] + 1: curr_run[1] = curr_level
		else: all_runs.append(curr_run); curr_run = [curr_level, curr_level]
	all_runs.append(curr_run)
	all_runs_str = ''
	for r in all_runs:
		if r[0] == r[1]: all_runs_str += str(r[0])
		else: all_runs_str += "%d-%d" % (r[0], r[1])
		all_runs_str += ', '
	return all_runs_str[:-2]

print
print "(level stats)"
print

kanji_only=True
# kanji_only=False

unburned_levels = []
all_levels = []
for u in all_item_objects.values():
	if u.level in unburned_levels: continue
	if kanji_only == True and u.type != 'kanji': continue
	all_levels.append(u.level)
	if u.srs_score < 9: unburned_levels.append(u.level)

curr_kanji_burned_levels = ( list( set(all_levels) - set(unburned_levels) ) )
# curr_everything_burned_levels = ( list( set(all_levels) - set(unburned_levels) ) )

print "levels cleared:", format_levels(curr_kanji_burned_levels),

if curr_kanji_burned_levels != prev_kanji_burned_levels:
	newly_burned_levels = ( list( set(curr_kanji_burned_levels) - set(prev_kanji_burned_levels) ) )
	print "(hey, new progress! congrats! on newly clearing %s)" % newly_burned_levels
	get_data.save_cornichon(curr_kanji_burned_levels, get_data.burned_levels_fn)
else: print



# below some even more specific stuff for me: how I further use kanji stats to track progress
# see https://codepen.io/tylergneill/full/MzYgry/

print "(for CodePen)"

total_kanji_enlightened = 0
total_kanji_burned = 0
for u in all_item_objects.values():
	if u.type == 'kanji' and u.srs_score >= 8:
		total_kanji_enlightened += 1
		if u.srs_score == 9:
			total_kanji_burned += 1

print "%03.1f%%" % (total_kanji_enlightened/1500.0*100)
print "'Enlightened'+ kanji: %d/1500 (%03.1f%%) (x1)" % (total_kanji_enlightened, (total_kanji_enlightened/1500.0*100) )
print "'Burned' kanji: %d/1500 (%03.1f%%)" % (total_kanji_burned, (total_kanji_burned/1500.0*100) )
print