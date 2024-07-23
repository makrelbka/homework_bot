import pickle
from data import *


def read_save():
    with open('save.pickle', 'rb') as f:
        try:
            D.data = pickle.load(f)
            D.suggestion = pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            D.data = {}
            for i in D.subjects:
                D.data.pop(i , "")
            D.suggestion = []

def edit_save():
    with open('save.pickle', 'wb') as f:
        pickle.dump(D.data, f)
        pickle.dump(D.suggestion, f)