import settings
import tweepy
import dataset

from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json

access_token = "XX"
access_token_secret = "XX"
consumer_key = "XX"
consumer_secret = "XX"



db = dataset.connect(settings.CONNECTION_STRING)

class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
        	if status.retweeted:
            		return

		tweet_date = status.created_at
		retweet_status = status.retweeted
		retweet_count = status.retweet_count
		fave_count = status.favorite_count
		tweet_source = status.source
		user_id_str = status.user.id_str
		username = status.user.name
		user_verified = status.user.verified
		user_descr = status.user.description
		user_creation_date = status.user.created_at
		user_location = status.user.location
		screenname = status.user.screen_name
		user_friend_count = status.user.friends_count
		tweet_text = status.text
		tweet_id = status.id
		source = status.source

	        table = db[settings.TABLE_NAME]
	        try:
	            table.insert(dict(
	                tweet_date=tweet_date,
	                retweet_status=retweet_status,
	                retweet_count=retweet_count,
	                fave_count=fave_count,
	                tweet_source=tweet_source,
	                user_id_str=user_id_str,
	                username=username,
	                user_verified=user_verified,
	                user_descr=user_descr,
	                user_creation_date=user_creation_date,
	                user_location=user_location,
	                screenname=screenname,
	                user_friend_count=user_friend_count,
			tweet_id = tweet_id,
			source = source,
	                tweet_text=tweet_text,
	            ))
	        except ProgrammingError as err:
	            print(err)

	def on_error(self, status_code):
	        if status_code == 420:
	            #returning False in on_data disconnects the stream
	            return False

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)

