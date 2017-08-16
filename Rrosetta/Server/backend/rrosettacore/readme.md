### Rrosetta Core Files

This is all the core functionality of the Rrosetta programme.<br />
The structure and purpose of each script is as follows:<br />

+ master_control.py is the overarching control script that triggers each of the others.
+ g_auth.py holds all the (broken) OAuth2 processes.
+ sent_mail.py uses the credentials and service built in g_ath.py to access all the Users sent emails. These are held in a set.
+ text_sum.py first builds a long string of all the emails combined. It then uses the Sumy text summeriser to recursively focus the emails down to a single sentence. [ VERY MUCH IN DEV ]
+ get_sentiment.py uses NLTK to read this sentence and returns the most important noun or nouns.
+ citation_json.py then builds a JSON file containing all the text and images from every page used as a reference citation on the Wikipedia entry for that noun.
+ img_anal.py does basic analysis on the images in a JSON file.
+ txt_anal.py does basic analysis on the text in a JSON file.