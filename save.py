import os
import pickle
from data import *


def read_save():
    if not os.path.exists('save.pickle') or os.path.getsize('save.pickle') == 0:
        D.data = {}
        D.suggestion = []
        for i in D.subjects:
            D.data[i] = ""
        return 
    with open('save.pickle', 'rb') as f:
        D.data = pickle.load(f)
        D.suggestion = pickle.load(f)
        if (D.data == {}):
            for i in D.subjects:
                D.data[i] = ""
            D.suggestion = []

def edit_save():
    with open('save.pickle', 'wb') as f:
        pickle.dump(D.data, f)
        pickle.dump(D.suggestion, f)

def clear():
    D.data = {}
    edit_save()
    