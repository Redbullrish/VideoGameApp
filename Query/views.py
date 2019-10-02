import os
import pandas as pd
import queue as Q
import math
from django.shortcuts import render


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class VG:

    def __init__(self,platform,genre,dev):
        self.platform = platform
        self.genre = genre
        self.dev = dev

def index(request):
    df = pd.read_csv(os.path.join(BASE_DIR, 'Query/data/video_game.csv'))
    game = VG("Wii","Sports","Nintendo")
    pq = Q.PriorityQueue()
    lu = 0
    lc = 0
    us = 0
    cs = 0
    for index, row in df.iterrows():
        console_score = 1 if row['Platform'] == game.platform else 0
        genre_score = 1 if row['Genre'] == game.genre else 0
        dev_score = 1 if row['Publisher'] == game.dev else 0
        critic_score = float(row['Critic_Score'])/1000.0
        if math.isnan(critic_score):
            critic_score = 0.0
        score = console_score + genre_score + dev_score + critic_score
        name = str(row['Name'])
        pq.put((-score,name))

    for i in range(10):
        print(pq.get())
    return render(request, 'index.html')
