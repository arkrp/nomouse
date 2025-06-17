import keyboard
from pynput.mouse import Button
from threading import Semaphore
import time
TIME_DELAY = 0.03
MOVEMENT_SPEED = 200
MOVEMENT_INCREMENT = TIME_DELAY * MOVEMENT_SPEED
def run_mode(callbacks, state):
    print('MOVE mode activated')
    running = True
    def cancel_loop(*ignored_args):
        nonlocal running
        running = False
    def press_left(*ignored_args):
        state['mouse'].press(Button.left)
    def release_left(*ignored_args):
        state['mouse'].release(Button.left)
    def press_right(*ignored_args):
        state['mouse'].press(Button.right)
    def release_right(*ignored_args):
        state['mouse'].release(Button.right)
    def press_alt(*ignored_args):
        keyboard.press('alt')
    keyboard.on_release_key('alt', cancel_loop, suppress=True) #you have to hold alt to stay in this mode
    keyboard.on_press_key('space', press_left, suppress=True) #space is for left click
    keyboard.on_release_key('space', release_left, suppress=True)
    keyboard.on_press_key('f', press_right, suppress=True) #f is for right click
    keyboard.on_release_key('f', release_right, suppress=True)
    keyboard.on_press_key('r', press_alt, suppress=True) #method of holding alt for other programs
    for letter in 'hjkl':
        keyboard.block_key(letter)
    while(running):
        time.sleep(TIME_DELAY)
        x_displacement, y_displacement = 0, 0
        if keyboard.is_pressed('j'):
            y_displacement = MOVEMENT_INCREMENT
        if keyboard.is_pressed('k'):
            y_displacement = -MOVEMENT_INCREMENT
        if keyboard.is_pressed('l'):
            x_displacement = MOVEMENT_INCREMENT
        if keyboard.is_pressed('h'):
            x_displacement = -MOVEMENT_INCREMENT
        state['mouse'].move(x_displacement, y_displacement)
        #TODO switch system to pynput because apparently keyboard (the library) does not suppress on linux and we already have pynput as a dependency
    release_left()
    release_right()
    print('MOVE mode deactivated')
    return 'IDLE'
def bind(func, args): #  
    # binds a function to always be called with specific parameters and to ignore any other arguments passed in.
    def return_value(*ignored_parameters):
        return func(*args)
    return return_value
# 
