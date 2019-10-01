import os
import pandas as pd
from django.shortcuts import render


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    df = pd.read_csv(os.path.join(BASE_DIR, 'Query/data/video_game.csv'))
    for index, row in df.iterrows():
        pass
    return render(request, 'index.html')
