This tiny library is meant to help download and manipulate WaniKani information offline. It's made for people like me who like to fiddle around with text files and spreadsheets, finding patterns, maybe seeing familiar material in different study environments (e.g. Anki, Quizlet). So what these scripts do is get a user's info from WaniKani and format it as simple tsv text files.

The most valuable thing here is the Python object structure corresponding to the item attributes. I happen to want to do certain things with this at the moment, including stuff with pitch accent, but enterprising users will modify the code to make it do what they want, and I hope the code is written clearly to help with this.

The parts work as follows:

* __get\_data.py__: Fetches information for user's unlocked subjects (= radicals, kanji, vocabulary), folds in pitch information for vocabulary, and saves a local version of the data for offline use. (Assisted by: pitches.txt, which is a modified version of the table in the 'WaniKani Pitch Info' userscript)

* __data\_store.p__: Stores subject info. (Assisted by: burned\_levels.p, which focuses on user's progress with kanji)

* __progress\_report.py__: Exports subject info as separate tsv files (one each for radicals, kanji, vocabulary). If you want less info than what is currently exported, just open the files as spreadsheets and delete unwanted columns. If you want more, or in a different format, then you can change the Python code. This script also summarizes kanji burn stats in the Terminal window, including whether any new levels cleared, which is a metric I happen to like.

How to use:

1. Clone repo.
2. Open get\_data.py in a text editor and add your API key where indicated. Alternatively, put it in a local text file (the default name being looked for is 'api_key.txt') and the script will find it.
3. At the terminal, run progress\_report.py.
4. Wait briefly for the data pull to complete, then look in the local directory for the exported tsv files. You can also read the kanji burn stats in the Terminal window if you're interested.
5. Once you figure out what you want it to do for you, change the code to suit your needs, and let me know if you come up with something good!