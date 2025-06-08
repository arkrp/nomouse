import keyboard
import time
def run_mode(callbacks):
    keyboard.add_hotkey('alt', callbacks['set_mode'], args=('CLICK',))
    time.sleep(7)
    try:
        if callbacks['get_mode']() == 'IDLE':
            callbacks['set_hidden'](True)
    except RuntimeError as e:
        raise RuntimeError('main thread was likely killed before timer completed. Probably fine.') from e
def bind(func, args):
    def return_value():
        return func(*args)
    return return_value

