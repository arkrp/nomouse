#  import stuff!
import keyboard
import time
from threading import Semaphore
from sys import exit
import mouse
#TODO, completely remove mouse import from this thread. mouse input scripts appear to have substantial problems with multi-threading. move everything to the main thread.
# 
gridcharacters = list('qwertyuiopasdfghjkl;zxcvbnm,./')
movement_duration = 0.1
def run_mode(callbacks): #  
    """this is mostly an ugly block of user input"""
    set_mode = callbacks['set_mode']
    set_status = callbacks['set_status']
    highlight_zone = highlight_zone_maker(callbacks['highlight'], *(callbacks['get_screen_resolution']()))
    screen_position = screen_position_maker(callbacks['highlight'], *(callbacks['get_screen_resolution']()))
    keyboard.add_hotkey('alt+ctrl', callbacks['exit_nomouse'])
    keyboard.add_hotkey('alt+tab', bind(set_mode, ('IDLE',)))
    #keyboard.add_hotkey('alt+space', bind(set_mode, ('START_DRAG',)))
    keyboard.on_press_key('esc', bind(set_mode, ('IDLE',)), suppress=True)
    read_single_token(['alt'])
    grid_position = ''
    #print(f'highlighting zone \'{grid_position}\'')
    highlight_zone(grid_position)
    valid_tokens = list('qwertyuiopasdfghjkl;zxcvbnm,./') + ['alt', 'space']
    token1 = read_single_token(valid_tokens)
    set_status(grid_position)
    if token1 == 'alt':
        mouse.move(*screen_position(grid_position), duration=movement_duration)
        pyautogui.moveTo(*screen_position(grid_position))
        print(f'moveing to zone {grid_position}')
        set_mode('IDLE')
        exit()
    elif token1 == 'space':
        #mouse.move(*screen_position(grid_position))
        callbacks['mouse_press']()
        #callbacks['mouse_release']()
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
    grid_position += token1
    highlight_zone(grid_position)
    token2 = read_single_token(valid_tokens)
    if token2 == 'alt':
        mouse.move(*screen_position(grid_position), duration=movement_duration)
        pyautogui.moveTo(*screen_position(grid_position))
        print(f'moving to zone {grid_position}')
        set_mode('IDLE')
        exit()
    elif token2 == 'space':
        #mouse.move(*screen_position(grid_position))
        callbacks['mouse_press']()
        #callbacks['mouse_release']()
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
    else:
        grid_position += token2
        set_status(grid_position)
    #print(f'highlighting zone \'{grid_position}\'')
    highlight_zone(grid_position)
    token3 = read_single_token(valid_tokens)
    if token3 == 'alt':
        mouse.move(*screen_position(grid_position), duration=movement_duration)
        print(f'moving to zone {grid_position}')
        set_mode('IDLE')
        exit()
    elif token3 == 'space':
        #mouse.move(*screen_position(grid_position))
        callbacks['mouse_press']()
        #callbacks['mouse_release']()
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
    else:
        grid_position += token3
        set_status(grid_position)
        print(f'click zone {grid_position}')
        set_mode('IDLE')
        exit()
# 
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
def highlight_zone_maker(highlight, screen_width, screen_height): #  
    def highlight_zone(grid_position):
        'highlights a zone specified by the selector characters'
        base_x, base_y = 0, 0
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
# 
grid_characters_flat = 'qwertyuiopasdfghjkl;zxcvbnm,./'
def flat_row_col(character): #  
    #gets the row and column of a character in flat orientation
    pos = grid_characters_flat.find(character)
    row = pos//10
    col = pos%10
    return row, col
# 
grid_characters_stacked = 'qwertasdfgzxcvbyuiophjkl;nm,./'
def stacked_row_col(character): #  
    #gets the row and column of a character in stacked orientation
    pos = grid_characters_stacked.find(character)
    row = pos//5
    col = pos%5
    return row, col
# 
def screen_position_maker(highlight, screen_width, screen_height): #  
    def screen_position(grid_position):
        'gets the true screen position from the grid position'
        base_x, base_y = 0, 0
        width_1, height_1 = screen_width//5, screen_height//6
        width_2, height_2 = screen_width//25, screen_height//36
        width_3, height_3 = screen_width//250, screen_height//108
        if len(grid_position)==0:
            return screen_width//2, screen_height//2
        row_1, col_1 = stacked_row_col(grid_position[0])
        base_x += col_1*width_1
        base_y += row_1*height_1
        if len(grid_position)==1:
            highlight((width_1, height_1, base_x, base_y, True))
            return base_x + width_1//2, base_y + height_1//2
        row_2, col_2 = stacked_row_col(grid_position[1])
        base_x += col_2*width_2
        base_y += row_2*height_2
        if len(grid_position)==2:
            return base_x + width_2//2, base_y + height_2//2
        row_3, col_3 = flat_row_col(grid_position[2])
        base_x += col_3*width_3
        base_y += row_3*height_3
        if len(grid_position)==3:
            return base_x + width_3//2, base_y + height_2//3
        raise ValueError(f'screen_position recieved invalid input {grid_position=}')
    return screen_position
# 


