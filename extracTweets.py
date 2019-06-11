from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

import twitterCredentials


class TweetListener(StreamListener):

    def on_data(self, raw_data):
        print(raw_data)
        return True

    def on_error(self, status_code):
        print(status_code)


if __name__ == "__main__":

    listener = TweetListener()
    authentication = OAuthHandler(twitterCredentials.consumerKey, twitterCredentials.consumerSecret)
    authentication.set_access_token(twitterCredentials.accessToken, twitterCredentials.accessTokenSecret)

    stream = Stream(authentication, listener)

    stream.filter(track=['huawei', 'apple'], locations=[-92.2072, -5.0159, -75.1925, 1.8836], languages=['es'])
