This tiny library is meant to help a user download and manipulate their WaniKani information offline. The default behavior is to export this info in the form of tsv text files, which can then easily be read directly in a text editor, or opened as a spreadsheet, or imported into Anki. By focusing on the ever-growing list of subjects a given person has been exposed to, this provides a uniquely relevant data set for supplementing individual learning (example use case: sorting vocabulary both by pitch accent class and by SRS progress).

The parts work as follows:

	get_data.py: Fetches information for user's unlocked subjects (= radicals, kanji, vocabulary), folds in pitch information for vocabulary (modified form of table in the 'WaniKani Pitch Info' userscript), and saves a local version of the data for offline use.
		[data.py, count_morae.py]

	data_store.p: Stores subject information (including pitch) and also remembers the levels on which all kanji burned (= my own single preferred metric of progress).
	(assisted by: count_morae.py, burned_levels.p)
		[burned_levels.p, all_items.p]

	progress_report.py: Exports subject info as three separate tsv files (change Python code to modify format) and also summarizes kanji burn stats, including whether any new levels cleared.
		[progress_report.py]

How to use:
	1) Clone repo.
	2) Open get_data.py in a text editor and add your API key.
	3) At the terminal, run progress_report.py.
	3) Wait for data pull to complete, read kanji burn stats in terminal window, then look in directory for exported tsv files.