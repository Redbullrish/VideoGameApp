import os
import sys
import pandas as pd
import queue as Q
import math

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from Query.forms import QueryForm


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

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            games = recommend(form.cleaned_data['genre'],form.cleaned_data['platform'])
            context = {
                'games':games,
            }
            return render(request, 'display.html', context)
    else:
        form = QueryForm()
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


def recommend(genre,platform):
    df = pd.read_csv(os.path.join(BASE_DIR, "Query/data/video_game.csv"))
    game = VG(platform,genre,"")
    pq = build_rank(df,game)
    games = []

    for i in range(10):
        games.append(pq.get()[1])
    df.set_index("Name", inplace=True)
    return games

def build_rank(df,game):
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