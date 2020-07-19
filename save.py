
import pickle

def load_state():
    global state 
    try:
        with open("save.p", 'rb') as f:
            state = pickle.load(f)
            f.close()
    except FileNotFoundError:
        state = {}
    except Exception as e:
        raise(e)

def save_state(param, value):
    global state
    state[param] = value
    with open("save.p", 'wb') as f:
        pickle.dump(state, f)
        f.close()
