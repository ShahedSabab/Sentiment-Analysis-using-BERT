# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 22:41:35 2020

@author: sabab
"""

import json
import pandas as pd
from tqdm import tqdm

import seaborn as sns
import matplotlib.pyplot as plt

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from google_play_scraper import Sort, reviews, app


def print_json(json_object):
    '''
    print json request
    '''
    json_str = json.dumps(json_object, indent = 2, sort_keys = True, default=str)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))


def format_title(title):
    '''
    format title of the app
    '''
    sep_index = title.find(':') if title.find(':') != -1 else title.find('-')
    if sep_index != -1:
        title = title[:sep_index]
    return title[:10]

#crete the list of apps by collecting the ids from google play
app_packages = [
        'com.getsomeheadspace.android',   #headspace
        'com.strava',                     #strava
        'com.endomondo.android',          #endomondo
        'com.myfitnesspal.android',       #myfitnesspal
        'com.alltrails.alltrails',        #all trails
        'com.onepeloton.callisto',        #peloton
        'com.sillens.shapeupclub',        #lifesum
        'com.winwalk.android',                  #paedometer winwalk
        'com.calm.android',                     #calm
        'com.fitbit.FitbitMobile'               #fitbit
        ]
app_infos = []

for ap in tqdm(app_packages):
    info = app(ap, lang = 'en', country = 'us')
    del info['comments']
    app_infos.append(info)


#check to see the json response     
print_json(app_infos[1])
 
#check the app icon list
fig, axis = plt.subplots(2, len(app_infos)//2)
for i, ax in enumerate(axis.flat):
    ai = app_infos[i]
    img = plt.imread(ai['icon'])
    ax.imshow(img)
    ax.set_title(format_title(ai['title']))
    ax.axis('off')


#create dataframe
df_app_infos = pd.DataFrame(app_infos)
df_app_infos.to_csv('app_info.csv', index=None, header=True)


#collect reviews

app_reviews = []

for ap in tqdm(app_packages):
    for score in list(range(1, 6)):
        for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
            rvs, _ = reviews(
            ap,
            lang='en',
            country='us',
            sort=sort_order,
            count= 200 if score == 3 else 100,
            filter_score_with=score
            )
            for r in rvs:
                r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
                r['appId'] = ap
            app_reviews.extend(rvs)
df_app_review = pd.DataFrame(app_reviews)
df_app_review.to_csv("app_reviews.csv", index=None, header=True)