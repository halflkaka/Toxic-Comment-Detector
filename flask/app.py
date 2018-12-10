# coding: utf-8
from flask import Flask, render_template, jsonify
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from config import CONF
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re, string
import pandas as pd, numpy as np
import json
import time

def tokenize(s): return re_tok.sub(r' \1 ', s).split()
re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

count = {'severe_toxic':10, 'obscene':10, 'threat':10, 'insult':10, 'identity_hate':10}

with open("vesc", "rb") as v:
	vec = pickle.load(v)

with open("model_param1", "rb") as file1:
	model1 = pickle.load(file1)

with open("model_param2", "rb") as file2:
	model2 = pickle.load(file2)

class listener(StreamListener):

    def __init__(self, time_limit=5):
        self.start_time = time.time()
        self.limit = time_limit
        super(listener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            all_data = json.loads(data)
            print(all_data)
            
            try:
                tweet = all_data["text"]
                data = [tweet]

                vectorized_data = vec.transform(data)
                preds = np.zeros(len(label_cols))
                for i in range(len(label_cols)):
                    preds[i] = model1[i].predict_proba(vectorized_data.multiply(model2[i]))[:,1]
                print (preds)
                if (preds[0] > 0.5):
                    print("it is toxic")
                    for i in range(1, len(preds)):
                        if (preds[i] > 0.3):
                            count[label_cols[i]] += 1
                print(tweet)
            except KeyError as e:
                pass
            return True
        else:
            return False

    def on_error(self, status):
        print (status)

def start():
	#consumer key, consumer secret, access token, access secret.
	ckey=CONF["APP_KEY"]
	csecret=CONF["APP_SECRET"]
	atoken=CONF["OAUTH_TOKEN"]
	asecret=CONF["OAUTH_TOKEN_SECRET"]

	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	twitterStream = Stream(auth, listener(time_limit=5))
	twitterStream.sample(languages=['en'])

# if __name__ == "__main__":
# 	start()

start()

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({'msg':'Hello'})

@app.route("/chart", methods=["GET"])
def getdata():
    res = []
    data = []
    bar = []
    for key in count:
        data.append({'key': key, 'value': count[key]})
        bar.append({'x': key, 'y': count[key]})
    res.append(data)
    res.append(bar)
    response = jsonify(res)
    print("resp: "+response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/refresh", methods=["GET"])
def refresh():
    start()
    res = []
    data = []
    bar = []
    for key in count:
        data.append({'key': key, 'value': count[key]})
        bar.append({'x': key, 'y': count[key]})
    # response = jsonify(data)
    res.append(data)
    res.append(bar)
    response = jsonify(res)
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run()


