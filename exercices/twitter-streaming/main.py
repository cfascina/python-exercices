from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import json
import pandas as pd

# Keys from Twitter App.
api_key = "7bh0n5ianppFnkNqPoQKst585"
api_key_secret = "hEw7ZEbkdYQDhloYrseNnilwrXiHARGMfMmf2QHQvJpKJepKVs"
access_token = "790554216750252032-CXPbxfjefy413MOiKfQYVA2HiZToqLB"
access_token_secret = "YmYuaXPOdCH3bW9VsK3o37PnK3cbWQwAeJia4uMgWRl61"

# Creates the authorization keys.
auth = OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# MongoDB connection.
server = MongoClient("localhost", 27017)
db = server.twitter_streaming
tweets_collected = db.tweets_collected


class TweetListener(StreamListener):
    def __init__(self):
        self.counter = 0

    def on_data(self, raw_data):
        tweet = json.loads(raw_data)
        created_at = tweet["created_at"]
        content = tweet["text"]

        tweet_obj = {
            "created_at": created_at,
            "content": content
        }

        if self.counter < 500:
            tweets_collected.insert_one(tweet_obj).inserted_id
            self.counter += 1
            return True
        else:
            return False


# Keywords to look for.
keywords = ["amazon forest", "carbon", "climate change", "tropical forest", "biodiversity"]

# Initialize Stream and StreamListener.
print("Establishing Twitter connection...", end = " ")
tweet_listener = TweetListener()
tweet_stream = Stream(auth, listener = tweet_listener)
print("Done.")

# Collects the tweets and disconnect.
print("Collecting tweets...", end = " ")
tweet_stream.filter(languages = ["en"], track = keywords)
tweet_stream.disconnect()
print("Done.")

# Creates a data set with collected tweets, convert it to a Pandas data frame and to a counter matrix.
print("Creating the data frame and matrices...", end = " ")
data_set = [{"created_at": item["created_at"], "content": item["content"]} for item in tweets_collected.find()]
data_frame = pd.DataFrame(data_set)
vector_count = CountVectorizer()
matrix = vector_count.fit_transform(data_frame.content)
print("Done.")

print("Analyzing words occurrence...", end = " ")
word_count = pd.DataFrame(vector_count.get_feature_names(), columns = ["words"])
word_count["count"] = matrix.sum(axis = 0).tolist()[0]
word_count = word_count.sort_values("count", ascending = False).reset_index(drop = True)
print("Done.")

print("Exporting CSV file...", end = " ")
word_count[:50].to_csv("words_occurrence.csv")
print("Done.")
