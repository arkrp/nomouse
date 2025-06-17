import keyboard
from pynput.mouse import Button
from threading import Semaphore
import time
import sys
TIME_DELAY = 0.03
MOVEMENT_SPEED = 200
SCROLL_SPEED = 10
MOVEMENT_INCREMENT = TIME_DELAY * MOVEMENT_SPEED
SCROLL_INCREMENT = TIME_DELAY * SCROLL_SPEED
def run_mode(callbacks, state):
    print('MOVE mode activated')
    running = True
    def cancel_loop(*ignored_args):
        nonlocal running
        running = False
    left_pressed = False
    def press_left(*ignored_args):
        nonlocal left_pressed
        left_pressed = True
        state['mouse'].press(Button.left)
    def release_left(*ignored_args):
        nonlocal left_pressed
        left_pressed = False
        state['mouse'].release(Button.left)
    right_pressed = False
    def press_right(*ignored_args):
        nonlocal right_pressed
        right_pressed = True
        state['mouse'].press(Button.right)
    def release_right(*ignored_args):
        nonlocal right_pressed
        right_pressed = False
        state['mouse'].release(Button.right)
    def press_alt(*ignored_args):
        keyboard.press('alt')
    exit_mark = False
    def quit_program(*ignored_args):
        # a callback can't actually quit the program so we just mark down to quit the program when this mode ends
        nonlocal exit_mark
        exit_mark = True
    keyboard.on_release_key('alt', cancel_loop, suppress=True) #you have to hold alt to stay in this mode
    keyboard.on_press_key('space', press_left, suppress=True) #space is for left click
    keyboard.on_release_key('space', release_left, suppress=True)
    keyboard.on_press_key('f', press_right, suppress=True) #f is for right click
    keyboard.on_release_key('f', release_right, suppress=True)
    keyboard.on_press_key('r', press_alt, suppress=True) #method of holding alt for other programs
    keyboard.on_press_key('q', quit_program, suppress=True) #method of holding alt for other programs
    for letter in 'qwertyuiop[]asdfghjkl;\'zxcvbnm,./':
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
        if keyboard.is_pressed('m'):
            state['mouse'].scroll(0,-SCROLL_INCREMENT)
        if keyboard.is_pressed(','):
            state['mouse'].scroll(0,SCROLL_INCREMENT)
        state['mouse'].move(x_displacement, y_displacement)
    if left_pressed:
        release_left()
    if right_pressed:
        release_right()
    if exit_mark == True:
        callbacks['exit_nomouse']()
        sys.exit()
    print('MOVE mode deactivated')
    return 'IDLE'
def bind(func, args): #  
    # binds a function to always be called with specific parameters and to ignore any other arguments passed in.
    def return_value(*ignored_parameters):
        return func(*args)
    return return_value
# 
