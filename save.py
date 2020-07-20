
import pickle

if not 'state' in vars():
    try:
        with open("save.p", 'rb') as f:
            state = pickle.load(f)
            f.close()
    except FileNotFoundError:
        state = {}

def save_state(param, value):
    global state
    state[param] = value
    with open("save.p", 'wb') as f:
        pickle.dump(state, f)
        f.close()
