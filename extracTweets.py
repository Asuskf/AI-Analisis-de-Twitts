# -*- coding: utf-8 -*-
from pymongo.mongo_client import MongoClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, cursor, API

import twitterCredentials
import pandas as pd
import json


class TwitterAuthenticator:
    @staticmethod
    def authenticate_twitter_app():
        authentication = OAuthHandler(twitterCredentials.consumerKey, twitterCredentials.consumerSecret)
        authentication.set_access_token(twitterCredentials.accessToken, twitterCredentials.accessTokenSecret)
        return authentication


class ExtractTweets():
    @staticmethod
    def stream_tweets(list_words):
        authentication = TwitterAuthenticator.authenticate_twitter_app()
        listener = TweetListener()
        stream = Stream(authentication, listener)
        stream.filter(track=list_words, locations=[-92.2072, -5.0159, -75.1925, 1.8836], languages=['es'])


class TweetListener(StreamListener):

    def on_data(self, raw_data):
        try:
            data = pd.read_json(raw_data, orient='columns')
            client = MongoClient('localhost', 27017)
            data_base = client['DB_DataSourceTweets']
            collection = data_base['Doc_Tweets']
            jsonData = json.loads(data.head(1).T.to_json()).values()
            new_tweet = collection.insert(jsonData)
            print(jsonData)
            return True

        except BaseException as e:
            print("Error en on_data: %s" % str(e))

    def on_error(self, status_code):
        if status_code == 420:
            return False
        print(status_code)


if __name__ == "__main__":

    listWords = ['huawei', 'apple']
    tweets = ExtractTweets()
    tweets.stream_tweets(listWords)


