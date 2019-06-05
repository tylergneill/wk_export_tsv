This tiny library is meant to help download and manipulate WaniKani information offline. It's made for people like me who like to fiddle around with text files and spreadsheets, finding patterns, maybe seeing similar material within multiple study environments (e.g. Anki, Quizlet). Basically, these scripts fetch a user's info from WaniKani (storing it locally in a mini-database for offline querying,) and format it as simple tsv text files.

The parts work as follows:

* __get\_data.py__: Fetches information for user's unlocked subjects (= radicals, kanji, vocabulary), creates Python objects for everything, folds in pitch information for vocabulary (optional — an example pet interest), and saves a local version of everything for offline use. (Assisted by: pitches.txt, which is a modified version of the table in the 'WaniKani Pitch Info' userscript.)

* __data\_store.p__: Stores subject data. (Assisted by: burned\_levels.p, which focuses on user's progress with kanji — another pet interest)

* __progress\_report.py__: Interface for the above, exports fetched subject info as separate tsv files (one each for radicals, kanji, vocabulary). These tsv files can be opened like spreadsheets, and you can delete columns you don't want. Or, just change the Python code. This script also summarizes kanji burn stats in the Terminal window, including whether any new levels have been cleared recently, which is a metric I happen to like.

How to use:

1. Clone repo.
2. Open get\_data.py in a text editor and add your API key where indicated. Alternatively, put it by itself in a text file (the default name being looked for is 'api_key.txt') in the same place as the script, and the script will find it.
3. At the terminal, run progress\_report.py.
4. Wait briefly for the data pull to complete, then look in the local directory for the exported tsv files. Some messages are printed in the Terminal window, too.