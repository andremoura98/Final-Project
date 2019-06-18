#-*- coding: utf-8 -*-
import csv
import json
import pickle

import credenciais
import numpy as np
import pandas as pd
import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


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
        #track=["a","de","o","com","um","uma","em","para","por","se","e","ou","que","eu"]

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
            all_data= json.loads(data.encode("utf-8", "ignore"))
            texto = all_data["text"].replace("\n", "\\n")
            nome = all_data["user"]["name"]
            local = all_data["user"]["location"]
            filtro = all_data["filter_level"]

            verificar = all_data["user"]["verified"]
            protecao = all_data["user"]["protected"]

            seguidores = all_data["user"]["followers_count"]
            amigos = all_data["user"]["friends_count"]
            listas = all_data["user"]["listed_count"]

            retweet = all_data["retweet_count"] #tweet numbers
            cometarios = all_data["reply_count"] # tweet numbers
            likes = all_data["favorite_count"] # tweet numbers

            dados = [texto , nome , local , filtro , verificar, seguidores, amigos, listas, retweet, protecao, cometarios, likes]

            with open(self.fetched_tweets_filename, 'a', encoding="utf-8") as tf:
                csv_writer = csv.writer(tf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(dados)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True


    def on_error(self, status):
        print(status)


if __name__ == '__main__':


    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["Portugal, Universidade da Beira Interior, UBI, ubi, Universidade Beira Interior, Beira Interior, de , o ,com,um,uma,em,para,por,se,ou,que,eu "]
    fetched_tweets_filename = "tweetspercomma.csv"
    #geodata = api.reverse_geocode(40.2860100, -7.5039600, 15000, 'city')
    twitter_streamer = TwitterStreamer()

    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)#geodata

    #lertweets = ReadData()
    #lertweets.LerFicheiro()

