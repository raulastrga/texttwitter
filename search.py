#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2016/IIMAS/UNAM
# ----------------------------------------------------------------------
from __future__ import division, print_function  # Python 2 users only
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import json
import os
import hashlib

import argparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
import pickle
import json
import numpy as np
import re
import sys

import config

#Cargando Modelo CountVectorizer
with open('Modelos/CountVectorizer.pkl', 'rb') as f:
    count_vect = pickle.load(f)

#Cargando Modelo SVM
with open('Modelos/SVM.pkl', 'rb') as f:
    clf = pickle.load(f)

#Diccionario para repetidos
Dicc = {}

def Predecir(data):
    Arreglo = []
    datos = json.loads(data)

    #Se eliminan las URLS
    Linea = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', 'http://link//', datos['text'].encode("utf-8"))

    Arreglo.append(Linea)

    X_test = Arreglo

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

    _tweet = {}
    _tweet["user"] = {}
    _tweet["user"]["name"] = datos["user"]["name"]
    _tweet["user"]["screen_name"] = datos["user"]["screen_name"]
    _tweet["user"]["profile_image_url_https"] = datos["user"]["profile_image_url_https"]
    _tweet["id_str"] = datos["id_str"]

    resultado = {'tweet': json.dumps(_tweet), 'resultado': {'alegria': Y_pred[0,0], 'enojo': Y_pred[0,1], 'miedo':Y_pred[0,2],
                                                'neutral': Y_pred[0,3], 'repulsion': Y_pred[0,4], 'sorpresa': Y_pred[0,5],
                                                'tristeza': Y_pred[0,6]}, 'error': 0}

    #-----------------
    return resultado

def EliminarRepetidos(data):
    #Elimina URLS
    data['text'] = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', 'http://link//', data['text'].encode("utf-8")).decode("utf-8")

    #Convierte a Hash
    hash_object = hashlib.md5(data['text'].encode("utf-8"))

    #INTENTA BUSCARLO, SI LO ENCUENTRA REPETIDO NO AGREGA, SINO LO ENCUENTRA AGREGA
    try:
        if(Dicc[hash_object.hexdigest()]) == 0:
            i = 1
            return True
    except:
        Dicc[hash_object.hexdigest()] = 0
        return False

def TiempoReal(Texto):
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)

    c = tweepy.Cursor(api.search,
                       q=Texto,
                       rpp=30,
                       result_type="recents",
                       lang=['es']).items(50)
    try:
        TweetsRetornar = []
        for tweet in c:

            data = tweet._json
            Repetido = EliminarRepetidos(data)

            jtweet=json.dumps(tweet._json)

            #print (jtweet)
            if Repetido == False:
                TweetsRetornar.append(Predecir(jtweet))
        return TweetsRetornar
    except BaseException as e:
        resultado = {'error':str(e)}
        return resultado

def Usuario(Usr):
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)

    api = tweepy.API(auth)

    c = tweepy.Cursor(api.user_timeline, screen_name = Usr, count = 30).items(50)

    try:
        TweetsRetornar = []
        for tweet in c:
            jtweet=json.dumps(tweet._json)
            #print (jtweet)
            TweetsRetornar.append(Predecir(jtweet))
        return TweetsRetornar
    except BaseException as e:
        resultado = {'error':str(e)}
        return resultado
