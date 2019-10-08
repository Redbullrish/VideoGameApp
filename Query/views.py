import os
import sys
import pandas as pd
import queue as Q
import math

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from Query.forms import GenreForm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVG_CRIT = 0.068
AVG_USR = 0.071

class VG:

    def __init__(self,platform,genre,dev):
        self.platform = platform
        self.genre = genre
        self.dev = dev

# Function to render Django forms
def query(request):

    form = GenreForm()
    context = {
        'form':form,
    }

    return render(request, 'query.html', context)

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def ingest(request):
    df = pd.read_csv(os.path.join(BASE_DIR, "Query/data/video_game.csv"))
    game = VG("PC","Puzzle","")
    pq = recommend(df,game)

    for i in range(10):
        print(pq.get()[1])
    df.set_index("Name", inplace=True)
    return render(request, 'index.html')

def recommend(df,game):
    pq = Q.PriorityQueue()

    for index, row in df.iterrows():
        console_score = 1 if row['Platform'] == game.platform else 0
        genre_score = 1 if row['Genre'] == game.genre else 0
        dev_score = 1 if row['Publisher'] == game.dev else 0

        critic_score = float(row['Critic_Score'])/1000.0
        if math.isnan(critic_score):
            critic_score = AVG_CRIT

        u = str(row['User_Score'])
        if isfloat(u) and not math.isnan(float(u)):
            s = float(row['User_Score'])
            user_score = s/100.0
        else:
            user_score = AVG_USR
        
        score = console_score + genre_score + dev_score + critic_score + user_score
        name = str(row['Name'])
        pq.put((-score,name))
    
    return pq