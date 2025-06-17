import keyboard
from threading import Semaphore
import time
def run_mode(callbacks, state):
    token = read_single_token(['alt'], suppressed_tokens=['alt'])
    return 'CLICK'
def bind(func, args):
    def return_value(*ignored_args):
        return func(*args)
    return return_value
def read_single_token(press_tokens=(), release_tokens=(), suppressed_tokens=(), on_release=False): #  
    # waits for a key to be pressed from valid tokens and then returns which one got pressed.
    signal = Semaphore(0)
    return_value = None
    def write_return_value(*value):
        nonlocal return_value
        return_value = ''.join(value)
        signal.release()
    for token in press_tokens:
        suppress = token in suppressed_tokens
        keyboard.on_press_key(token, bind(write_return_value, (token)), suppress=suppress) #treat int creation as a nop
    for token in release_tokens:
        suppress = token in suppressed_tokens
        keyboard.on_release_key(token, bind(write_return_value, (token)), suppress=suppress)
    signal.acquire()
    for token in press_tokens:
        keyboard.unhook(token)
    for token in release_tokens:
        keyboard.unhook(token)
    return return_value
# 

