import keyboard
import time
from threading import Semaphore
from sys import exit
gridcharacters = list('qwertyuiopasdfghjkl;zxcvbnm,./')
def run_mode(callbacks):
    """this is mostly an ugly block of user input"""
    set_mode = callbacks['set_mode']
    set_status = callbacks['set_status']
    highlight_zone = highlight_zone_maker(callbacks['highlight'], *(callbacks['get_screen_resolution']()))
    keyboard.add_hotkey('alt+ctrl', callbacks['exit_nomouse'])
    keyboard.add_hotkey('alt+tab', bind(set_mode, ('IDLE',)))
    keyboard.on_press_key('esc', bind(set_mode, ('IDLE',)), suppress=True)
    read_single_token(['alt'])
    grid_position = ''
    #print(f'highlighting zone \'{grid_position}\'')
    highlight_zone(grid_position)
    valid_tokens = list('qwertyuiopasdfghjkl;zxcvbnm,./') + ['alt']
    token1 = read_single_token(valid_tokens)
    grid_position += token1
    set_status(grid_position)
    if token1 == 'alt':
        set_mode('START_DRAG')
        exit()
    #print(f'highlighting zone \'{grid_position}\'')
    highlight_zone(grid_position)
    valid_tokens = list('qwertyuiopasdfghjkl;zxcvbnm,./') + ['alt','space']
    token2 = read_single_token(valid_tokens)
    if token2 == 'alt':
        print(f'move zone {grid_position}')
        set_mode('IDLE')
        exit()
    elif token2 == 'space':
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
    else:
        grid_position += token2
        set_status(grid_position)
    #print(f'highlighting zone \'{grid_position}\'')
    highlight_zone(grid_position)
    valid_tokens = list('qwertyuiopasdfghjkl;zxcvbnm,./') + ['alt','space']
    token3 = read_single_token(valid_tokens)
    if token3 == 'alt':
        print(f'move zone {grid_position}')
        set_mode('IDLE')
        exit()
    elif token3 == 'space':
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
    else:
        grid_position += token3
        set_status(grid_position)
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
def hello(): #  
    # says hello!
    print('hello!')
# 
def bind(func, args): #  
    # binds a function to always be called with specific parameters and to ignore any other arguments passed in.
    def return_value(*ignored_parameters):
        return func(*args)
    return return_value
# 
def read_single_token(valid_tokens): #  
    # waits for a key to be pressed from valid tokens and then returns which one got pressed.
    signal = Semaphore(0)
    return_value = None
    def write_return_value(*value):
        nonlocal return_value
        return_value = ''.join(value)
        signal.release()
    for token in valid_tokens:
        keyboard.on_press_key(token, bind(int, ()), suppress=True) #treat int creation as a nop
        keyboard.on_release_key(token, bind(write_return_value, (token)), suppress=True)
    signal.acquire()
    for token in valid_tokens:
        keyboard.unhook(token)
    return return_value
# 
def highlight_zone_maker(highlight, screen_width, screen_height):
    def highlight_zone(grid_position):
        'highlights a zone specified by the selector characters'
        base_x, base_y = 0, 0
        print(f'{screen_width=} {screen_height=}')
        width_1, height_1 = screen_width//5, screen_height//6
        width_2, height_2 = screen_width//25, screen_height//36
        if len(grid_position)==0:
            highlight((screen_width, screen_height, base_x, base_y, True))
            return
        row_1, col_1 = stacked_row_col(grid_position[0])
        base_x += col_1*width_1
        base_y += row_1*height_1
        if len(grid_position)==1:
            highlight((width_1, height_1, base_x, base_y, True))
            return
        row_2, col_2 = stacked_row_col(grid_position[1])
        base_x += col_2*width_2
        base_y += row_2*height_2
        if len(grid_position)==2:
            highlight((width_2, height_2, base_x, base_y, True))
            return
    return highlight_zone
grid_characters_flat = 'qwertyuiopasdfghjkl;zxcvbnm,./'
def flat_row_col(character):
    #gets the row and column of a character in flat orientation
    pos = grid_characters_flat.find(character)
    row = pos//10
    col = pos%10
    return row, col
grid_characters_stacked = 'qwertasdfgzxcvbyuiophjkl;nm,./'
def stacked_row_col(character):
    #gets the row and column of a character in stacked orientation
    pos = grid_characters_stacked.find(character)
    row = pos//5
    col = pos%5
    return row, col

