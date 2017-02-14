#!/usr/bin/python
import MySQLdb
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db_mysql = MySQLdb.connect('141.118.3.90','mendelchan','chanmq21','WordsDisambiguation_b4')

fd = open("../Spots_tagme_nofilter", "r")
contents = fd.readlines()
spotsAll = [c.strip("\n").split("\t")[0] for c in contents]


db_mysql.ping()
cursor = db_mysql.cursor()
getTweets = "SELECT TEXT FROM Tweets WHERE Processed is NULL"
cursor.execute(getTweets)
tweetsRaw = cursor.fetchall()
tweets = [tweet[0] for tweet in tweetsRaw]

words = []
for tweet in tweets:
	wordList = tweet.split(" ")
	for word in wordList:
		try:
				if not word.startswith("http") and word.encode('latin-1','ignore') not in words:
					words.append(word.encode('latin-1','ignore'))
		except:
			pass
print words
print len(words)
insert = ""
for word in words:
	insert += "(\'" + word + "\')," 

insert = insert[:-1]
sql = "INSERT IGNORE INTO Words(Word) VALUES " + insert
print sql
cursor.execute(sql)
db_mysql.commit()