#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Raúl Astorga Castro // raulastorga@openmailbox.org
# ----------------------------------------------------------------------

# Cargando librerias
from __future__ import division, print_function  # Python 2 users only
import argparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import config2 as config
import pickle
import json
import numpy as np
import re

def Predecir(X_test):
    Clases =["Alegria", "Enojo", "Miedo", "Neutral", "Repulsion", "Sorpresa", "Tristeza"]
    X_test = np.array(X_test)
    #Se crea el arreglo con la cuenta de las palabras
    X_test = count_vect.transform(X_test)

    #Predecir directo a un resultado
    #Y_pred=clf.predict(X_test)
    #print ("Resultado: ", Clases[Y_pred[0]-1])
    #-------------------

    #Predecir con probabilidades
    Y_pred=clf.predict_proba(X_test)
    Y_pred = np.array(Y_pred)

    print ("Resultado: ")
    print ("Alegria: \t", round(Y_pred[0,0]*100, 2), "%")
    print ("Enojo: \t\t", round(Y_pred[0,1]*100, 2), "%")
    print ("Miedo: \t\t", round(Y_pred[0,2]*100, 2), "%")
    print ("Neutral: \t", round(Y_pred[0,3]*100, 2), "%")
    print ("Repulsion: \t", round(Y_pred[0,4]*100, 2), "%")
    print ("Sorpresa: \t", round(Y_pred[0,5]*100, 2), "%")
    print ("Tristeza: \t", round(Y_pred[0,6]*100, 2), "%")
    #-----------------

    print ("\n")
    time.sleep(5)

class Collector(StreamListener):
    def on_data(self, data):
        try:
            Arreglo = []
            datos = json.loads(data)

            print ("===========================================================================")
            print(datos['text'].encode('utf-8'))
            print ("===========================================================================")

            #Se eliminan las URLS
            Linea = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', 'http://link//', datos['text'].encode("utf-8"))

            Arreglo.append(Linea)
            Predecir(Arreglo)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(15)
        return True

    def on_error(self, status):
        print(status)
        return True


def Iniciar():
    #Cargando Modelo CountVectorizer
    with open('CountVectorizer.pkl', 'rb') as f:
        count_vect = pickle.load(f)

    #Cargando Modelo SVM
    with open('SVM.pkl', 'rb') as f:
        clf = pickle.load(f)

    #Obteniendo Tweets en tiempo real
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth=auth, listener=Collector())
    twitter_stream.filter(track=['de'], languages=["es"])
