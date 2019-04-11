#-*- coding: utf-8 -*-
import tweepy
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
import numpy as np
import pandas as pd
import credenciais
import codecs as cc
import json
class TwitterAutentificacao():

    def autentificar_app_twitter(self):
        auth = OAuthHandler(credenciais.Consumer_key, credenciais.Consumer_secret_key)
        auth.set_access_token(credenciais.Access_Token, credenciais.Access_Secret_Token)
        return auth

class TwitterStreamer():# Proccesamento e stream de tweets
    # construtor
    def __init__(self):
        self.autentificador_twitter= TwitterAutentificacao()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):  # geodata

        listener = StdOutListener(fetched_tweets_filename)
        auth= self.autentificador_twitter.autentificar_app_twitter()
        stream = Stream(auth, listener)
        #track=["a","de","o","com","um","uma","em","para","por","se","e","ou","que","eu"])

        # Filtragem dos tweets por palavras-chave
        stream.filter(track=hash_tag_list, languages=["pt"])


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:

            all_data= json.loads(data)
            texto = all_data["text"]

            print(texto)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(texto)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True


    def on_error(self, status):
        print(status)

#class TweetAnalyzer():
 #   def tweets_categorizados(self,data):
  #      df = pd.DataFrame(data=[tweet.txt for tweet in data], columns=['data'])
   #     return df

if __name__ == '__main__':

    #tweet_analyzer =  TweetAnalyzer()
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["Covilhã, Universidade da Beira Interior, UBI, ubi, Universidade Beira Interior"]
    fetched_tweets_filename = "tweets.json"
    #geodata = api.reverse_geocode(40.2860100, -7.5039600, 15000, 'city')
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)#geodata
    #df = tweet_analyzer.tweets_categorizados(data=[])
    #print(df)
