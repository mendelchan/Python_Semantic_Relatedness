#!/usr/bin/python
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import MySQLdb,re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
db_CikmTwitterDataSet = MySQLdb.connect('141.118.3.90','mendelchan','chanmq21','WordsDisambiguation_b4')
def main():
	# keep detecting if a tweet is processed or not
	count = 1
	while(True):
		# query - get tweets that have not been processed: SELECT Tweets.Id from Tweets WHERE Tweets.Id NOT IN (SELECT TweetsWords.TweetId FROM TweetsWords) limit 100;
		db_CikmTwitterDataSet.ping(True)
		cursor = db_CikmTwitterDataSet.cursor()
		query_lock_table = "LOCK TABLES Tweets WRITE"
		cursor.execute(query_lock_table)
		query_getTweets = "SELECT Tweets.TweetId, Tweets.Text from Tweets WHERE Processed is Null"
		cursor.execute(query_getTweets)
		tweetsId_list_pre = cursor.fetchall()
		tweetsId_Text_hash = {}
		tweetsId_string = "("
		for item in tweetsId_list_pre:
			tweetsId_Text_hash[item[0]] = item[1]
			tweetsId_string += str(item[0])
			tweetsId_string += ","
		if len(tweetsId_string) > 1:
			tweetsId_string = tweetsId_string[:-1]
			tweetsId_string += ")"
			#print tweetsId_string
			query_update_processed = "UPDATE Tweets SET Processed=1 WHERE TweetId IN " + tweetsId_string
			#print query_update_processed
			cursor.execute(query_update_processed)
			query_unlock_table = "UNLOCK TABLES"
			cursor.execute(query_unlock_table)
			cursor.close()
		else:
			break


		# process each tweet from previous step and insert into TweetsWords table
		for TweetId in tweetsId_Text_hash:
				Text_Raw = tweetsId_Text_hash[TweetId]
				Text_Raw_list = Text_Raw.split(" ")
				#print Text_Raw_list
				StartIndex = 0
				EndIndex = 0
				for i in range(len(Text_Raw_list)):
						word_raw = Text_Raw_list[i]
						IsHashtag = 0
						IsUrl = 0
						WordId = 0
					# query - insert into TweetsWords table: INSERT INTO TweetsWords (TweetId,WordId,Word,StartIndex,EndIndex,IsHashtag,IsUrl) SELECT TweetId, w.Id, Word, StartIndex, EndIndex, IsHashtag, IsUrl from Words w WHERE w.Word = Word_stemmed;
						try:
							db_CikmTwitterDataSet.ping(True)
							cursor = db_CikmTwitterDataSet.cursor()
							insertTweetsWords = "INSERT INTO TweetsWords (TweetId,WordId,Word,StartIndex,EndIndex,IsHashtag,IsUrl) SELECT " + str(TweetId) + ",w.Id," + "\"" + str(word_raw.encode('latin-1','ignore')) + "\"" + "," + str(StartIndex) + "," + str(EndIndex) + "," + str(IsHashtag) + "," + str(IsUrl) + " from Words w WHERE w.Word =" + "\'" + str(word_raw) + "\'"
							cursor.execute(insertTweetsWords)
							cursor.close()
							db_CikmTwitterDataSet.commit()
						except:
							#print TweetId
							db_CikmTwitterDataSet.rollback()
				# for next word's start index
		print count*1000
		count += 1
		sys.stdout.flush()
				
					
					
main()