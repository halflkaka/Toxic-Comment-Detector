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
import pathConfig
import cli
import sys

def tokenize(s): return re_tok.sub(r' \1 ', s).split()
re_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')
label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

colors = ['#6dc0ec', '#62acd4', '#5799bc', '#4c86a5', '#41738d', '#366076', '#2b4c5e', '#203946']

count = {'severe_toxic':0, 'obscene':0, 'threat':0, 'insult':0, 'identity_hate':0}
users = {'severe_toxic':[], 'obscene':[], 'threat':[], 'insult':[], 'identity_hate':[]}
county = {}
countState = {}#{'New York': {'name': 'New York', 'values':[{'label': "Toxic comment", 'val': 10}], 'color': colors[1]}}

with open("vesc", "rb") as v:
    vec = pickle.load(v)

with open("model_param1", "rb") as file1:
    model1 = pickle.load(file1)

with open("model_param2", "rb") as file2:
    model2 = pickle.load(file2)

class listener(StreamListener):

    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        super(listener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            all_data = json.loads(data)
            location = getLocation(all_data)
            if (type(location) != type(count)):
                print(location.country)

            try:
                tweet = all_data["text"]
                data = [tweet]

                vectorized_data = vec.transform(data)
                preds = np.zeros(len(label_cols))
                for i in range(len(label_cols)):
                    preds[i] = model1[i].predict_proba(vectorized_data.multiply(model2[i]))[:,1]
                if (preds[0] > 0.5):
                    print("it is toxic")
                    if (type(location) != type(count) and location.country == 'United States'):
                        state = location.state
                        if (state in countState):
                            countState[state]['val'] += 1
                        else:
                            countState[state] = {'label': "Toxic comment", 'val': 1}
                        ll = []
                        ll.append(countState[state])

                        index = countState[state]['val']

                        if index < 14:
                            color = colors[index//2]
                        else:
                            color = colors[7]

                        county[state] = {'name': state, 'values': ll, 'color': color}

                    for i in range(1, len(preds)):
                        if (i == 2 and preds[i] > 0.8):
                            count[label_cols[i]] += 1
                            user = {'name': all_data["user"]["name"], "tweet": all_data["text"]}
                            users[label_cols[i]].append(user)
                        elif (i != 2 and i != 4 and preds[i] > 0.1):
                            count[label_cols[i]] += 1
                            user = {'name': all_data["user"]["name"], "tweet": all_data["text"]}
                            users[label_cols[i]].append(user)
                        elif (i == 4 and preds[i] > 0.4):
                            count[label_cols[i]] += 1
                            user = {'name': all_data["user"]["name"], "tweet": all_data["text"]}
                            users[label_cols[i]].append(user)
                # print(tweet)
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

    twitterStream = Stream(auth, listener(time_limit=60))
    twitterStream.sample(languages=['en'])

def getdata():
    res = []
    data = []
    bar = []
    blacklist = []
    states = []
    for key in count:
        data.append({'key': key, 'value': count[key]})
        bar.append({'x': key, 'y': count[key]})
    res.append(data)
    res.append(bar)
    blacklist.append(users)
    res.append(blacklist)

    for key in county:
        states.append(county[key])

    res.append(states)
    print("states" + str(states))
    response = jsonify(res)
    return response

def getLocation(data):
    '''
    output_file = "tweet.json"
    input_file = "tweetLocation.json"
    with open(output_file, 'w') as fo:
        json.dump(data, fo)
    '''
    ok, result = cli.main(data)
    if ok:
        #with open(input_file, 'r') as fi:
            #result = json.load(fi)
        return result['location']
    else:
        return {}

start()

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({'msg':'Hello'})

@app.route("/chart", methods=["GET"])
def run():
    response = getdata()
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/refresh", methods=["GET"])
def refresh():
    start()
    response = getdata()
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run()


