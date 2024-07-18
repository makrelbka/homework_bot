import pickle

def read_save():
    with open('save.pickle', 'rb') as f:
        try:
            data = pickle.load(f)
            suggestion = pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            data = {"матан": "", "линал": "", "forFun": ""}
            suggestion = []
    return data, suggestion

def edit_save(data, suggestion):
    with open('save.pickle', 'wb') as f:
        pickle.dump(data, f)
        pickle.dump(suggestion, f)
