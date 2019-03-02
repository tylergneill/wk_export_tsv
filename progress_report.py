import data
from collections import OrderedDict

# RENAME AS JUST OUTPUT_TSV
def output_tsv_kanji_character_meaning(all_items, score_range=(1,9)):
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
			for u in all_items.values():
				if u.type != type or u.srs_score != score: continue
				if type == 'radical':
					out_str = str(u.level) + '\t' + u.meaning + '\n'
				elif type == 'kanji':
					out_str = str(u.level) + '\t' + u.character + '\t' + u.meaning + '\n'
				elif type == 'vocab':
					out_str = str(u.level) + '\t' + u.character + '\t' + u.meaning + '\n'
				out_f.write(out_str.encode('utf-8'))
		out_f.close()

def which_levels_unburned(all_items, kanji_only=True):
	unburned_levels = []
	for u in all_items.values():
		if u.level in unburned_levels: continue
		if kanji_only and u.type != 'kanji': continue
		if u.srs_score < 9: unburned_levels.append(u.level)
	return unburned_levels

def format_runs(levels):
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


# initialize with level details

curr_learning_level = data.load_cornichon(data.learning_level_fn, int())
if curr_learning_level == 0:
	curr_learning_level = int(raw_input("(psst? which level?) "))
	data.save_cornichon(curr_learning_level, data.learning_level_fn)

print
print "current known learning level =", curr_learning_level
choice = raw_input("leveled up and working on next now? (Y/n)")
if choice == 'Y':
	curr_learning_level += 1
	data.save_cornichon(curr_learning_level, data.learning_level_fn)
	print "current learning level now:", curr_learning_level

prev_kanji_burned_levels = data.load_cornichon(data.burned_levels_fn, list())
print "levels known so far with all kanji burned are:", format_runs(prev_kanji_burned_levels)

working_levels = range(1, curr_learning_level+1)
for l in prev_kanji_burned_levels: working_levels.remove(l) # inverse
print "currently working on levels:", format_runs(working_levels)

# load saved item object data
prev_item_objects = data.load_cornichon(data.all_items_fn, OrderedDict())

# REPHRASE AS GET ANY INFO OR NOT
choice = raw_input('get data for working levels? (Y/n)')
if choice == 'Y':

	# pull updated info and save
	# MAKE THIS THE ONLY SOURCE OF INFO GOING FORWARD
	new_item_objects = data.pull_progress(working_levels)

	# consolidate previous and new objects
	# ELIMINATE THIS STEP
	all_items = data.consolidate_objects(
		base=prev_item_objects, additions=new_item_objects)

	# save updated info
	data.save_cornichon(all_items, data.all_items_fn)

else: all_items = prev_item_objects

# output object info to tsv files
output_tsv_kanji_character_meaning(all_items, score_range=(1,9)) # (1,9) all; (5,6) guru

# report if additional levels now fully burned

# SHOULDN'T NEED TO AVOID THESE
all_but_last_levels = range(1, max(2,curr_learning_level-3)) # don't bother checking last few, in case of errors...

curr_kanji_unburned_levels = which_levels_unburned(all_items, kanji_only=True)
curr_kanji_burned_levels = ( list( set(all_but_last_levels) - set(curr_kanji_unburned_levels) ) )

curr_anything_unburned_levels = which_levels_unburned(all_items, kanji_only=False)
curr_everything_burned_levels = ( list( set(all_but_last_levels) - set(curr_anything_unburned_levels) ) )

total_kanji_enlightened = 0
total_kanji_burned = 0
for u in all_items.values():
	if u.type == 'kanji' and u.srs_score >= 8:
		total_kanji_enlightened += 1
		if u.srs_score == 9:
			total_kanji_burned += 1

if curr_kanji_burned_levels != prev_kanji_burned_levels:
	print "hey! now levels with totally burned kanji are:", format_runs(curr_kanji_burned_levels)
	if curr_everything_burned_levels != []:
		print "of which, levels with everything burned are:", format_runs(curr_everything_burned_levels)
	data.save_cornichon(curr_kanji_burned_levels, data.burned_levels_fn)

print 
print "(for CodePen)"
print
print "%03.1f%%" % (total_kanji_enlightened/1500.0*100)
print "'Enlightened'+ kanji: %d/1500 (%03.1f%%) (x1)" % (total_kanji_enlightened, (total_kanji_enlightened/1500.0*100) )
print "'Burned' kanji: %d/1500 (%03.1f%%)" % (total_kanji_burned, (total_kanji_burned/1500.0*100) )
print