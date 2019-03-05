This tiny library is meant to help a user download and manipulate their WaniKani information offline. It's made for someone like me who likes to fiddle around with text files and spreadsheets, finding patterns, maybe studying in different contexts (e.g. Anki, Quizlet). So, these scripts get the info from WaniKani specific to your study and format it as tsv text files. I've recently taken an interest in pronunciation and pitch accent, so I'm including that info in the vocabulary output, too.

The parts work as follows:

* __get\_data.py__: Fetches information for user's unlocked subjects (= radicals, kanji, vocabulary), folds in pitch information for vocabulary, and saves a local version of the data for offline use. (Assisted by: pitch\_patterns.txt, which is a modified version of the table in the 'WaniKani Pitch Info' userscript; and count\_morae.py, which calculates the number of morae in each word)

* __data\_store.p__: Stores subject info. (Assisted by: burned\_levels.p, which focuses on user's progress with kanji)

* __progress\_report.py__: Exports subject info as three separate tsv files. If you want less info, just open the files as spreadsheets and delete unwanted columns. If you want more, or in a different format, change the Python code. This also summarizes kanji burn stats in the Terminal, including whether any new levels cleared.

How to use:
1. Clone repo.
2. Open get\_data.py in a text editor and add your API key where indicated. Alternatively, put it in a local file 'api_key.txt', and the script will find it.
3. At the terminal, run progress\_report.py.
4. Wait for data pull to complete, then look in directory for exported tsv files. Read kanji burn stats in the terminal window if you're interested.