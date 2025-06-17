import keyboard
import time
def run_mode(callbacks, state):
    keyboard.press('alt')
    keyboard.press('tab')
    running=True
    def exitmode(*ignored_args):
        nonlocal running
        running = False
    keyboard.on_release_key('alt', exitmode)
    while(running):
        time.sleep(0.03)
    return 'IDLE'

