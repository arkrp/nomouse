#  import stuff!
import keyboard
import time
from pynput.mouse import Button
from threading import Semaphore
from sys import exit
# 
grid_characters = list('qwertyuiopasdfghjkl;zxcvbnm,./')
movement_duration = 0.1
def run_mode(callbacks, state): #  
    print('entering click')
    """this is mostly an ugly block of user input"""
    set_status = callbacks['set_status']
    mouse = state['mouse']
    highlight_zone = highlight_zone_maker(callbacks['highlight'], *(callbacks['get_screen_resolution']()))
    screen_position = screen_position_maker(callbacks['highlight'], *(callbacks['get_screen_resolution']()))
    grid_position = ''
    highlight_zone(grid_position)
    valid_tokens = grid_characters + ['alt', 'space', 'shift', '\'']
    suppressed_tokens=valid_tokens + ['tab', 'ctrl']
    token1 = read_single_token(grid_characters+['alt', 'space', 'shift', '\'', 'tab'], suppressed_tokens=suppressed_tokens)
    set_status(grid_position)
    if token1 == 'alt':
        return 'MOVE'
    if token1 == 'tab':
        return 'ALTTAB'
    elif token1 == 'space':
        highlight_zone(None)
        mouse.click(Button.left, 1)
        print('plain position click')
        return 'IDLE'
    elif token1 == 'shift':
        highlight_zone(None)
        mouse.click(Button.right, 1)
        print('position right click')
        return 'IDLE'
    elif token1 == '\'':
        highlight_zone(None)
        mouse.press(Button.left)
        read_single_token(release_tokens=('\''), suppressed_tokens=suppressed_tokens)
        print('position start drag')
        return 'CLICK'
    grid_position += token1
    highlight_zone(grid_position)
    token2 = read_single_token(valid_tokens, suppressed_tokens=suppressed_tokens)
    if token2 == 'alt':
        mouse.position = screen_position(grid_position)
        print(f'moving to zone {grid_position}')
        return 'IDLE'
    elif token2 == 'space':
        highlight_zone(None)
        mouse.position = screen_position(grid_position+'c')
        mouse.click(Button.left, 1)
        print(f'click zone {grid_position}')
        return 'IDLE'
    elif token2 == 'shift':
        highlight_zone(None)
        mouse.position = screen_position(grid_position+'c')
        mouse.click(Button.right, 1)
        print(f'right click zone {grid_position}')
        return 'IDLE'
    elif token2 == '\'':
        highlight_zone(None)
        mouse.position = screen_position(grid_position+'c')
        mouse.press(Button.left)
        read_single_token(release_tokens=('\''), suppressed_tokens=suppressed_tokens)
        print('position start drag')
        return 'CLICK'
    else:
        grid_position += token2
        set_status(grid_position)
    highlight_zone(grid_position)
    token3 = read_single_token(valid_tokens, suppressed_tokens=suppressed_tokens)
    if token3 == 'alt':
        mouse.position = screen_position(grid_position)
        print(f'moving to zone {grid_position}')
        return 'IDLE'
    elif token3 == 'space':
        highlight_zone(None)
        mouse.position = screen_position(grid_position)
        mouse.click(Button.left, 1)
        print(f'click zone {grid_position}')
        return 'IDLE'
    elif token3 == 'shift':
        highlight_zone(None)
        mouse.position = screen_position(grid_position)
        mouse.click(Button.right, 1)
        print(f'right click zone {grid_position}')
        return 'IDLE'
    elif token3 == '\'':
        highlight_zone(None)
        mouse.position = screen_position(grid_position)
        mouse.press(Button.left)
        read_single_token(release_tokens=('\''), suppressed_tokens=suppressed_tokens)
        print('position start drag')
        return 'CLICK'
    else:
        grid_position += token3
        set_status(grid_position)
        highlight_zone(None)
        mouse.position = screen_position(grid_position)
        mouse.click(Button.left, 1)
        print(f'click zone {grid_position}')
        return 'IDLE'
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
def highlight_zone_maker(highlight, screen_width, screen_height): #  
    def highlight_zone(grid_position):
        if(grid_position==None):
            highlight((0,0,0,0,False))
            return
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


