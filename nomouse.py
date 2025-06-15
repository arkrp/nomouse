#  setup
""" #  
nomouse.py

a program for making sure you, yes you, never need to use a mouse.

the main file is mostly just a whole bunch of bindings to let our mode runners easily call functions to do things. This is needed because tk desperately loves the main thread and its only thread safe call is to send an event to its main thread.
"""
# 
#  import stuff
import tkinter as tk
from tkinter import ttk
from tkinter import font
from threading import Thread
import keyboard
from pynput.mouse import Controller
import time
# 
#  define the modes
from modes.IDLE import run_mode as IDLE
from modes.CLICK import run_mode as CLICK
mode_runners = {'IDLE':IDLE,'CLICK':CLICK}
# 
#  create state
state = {'current_mode':'', 'status_text':'', 'statusbar_hidden':False , 'highlight':(400,400,400,400,True), 'mouse_x_pos':100, 'mouse_y_pos':100}
# 
# 
#  create GUI elements
#  make the statusbar
statusbar = tk.Tk()
screen_width = statusbar.winfo_screenwidth()
screen_height = statusbar.winfo_screenheight()
bar_width = 300
bar_height = 30
edge_offset = 10
statusbar.geometry(f'{bar_width}x{bar_height}+{edge_offset}+{screen_height - bar_height - edge_offset}')
statusbar.attributes('-topmost', 1)
statusbar.overrideredirect(1)
label = ttk.Label(statusbar, text='Link Start!', font=('Cascadia Mono', 19))
label.grid(column=0, row=0)
# 
#  make the highlight
highlight_window = tk.Toplevel()
highlight_window.wm_attributes('-alpha', 0.8)
highlight_window.attributes('-topmost', 1)
highlight_window.overrideredirect(1)
highlight_window.geometry(f"{10}x{10}+{10}+{10}")
# 
# 
#  create interface
#  create helper functions
def update_mouse_pos(): #  
    mouse.move(state['mouse_x_pos'], state['mouse_y_pos'])
# 
# 
#  make event stuff for gui
#  create event handlers!
def handle_refresh_statusbar(event): #  
    label.config(text=f'<{state['current_mode']}>{state['status_text']}')
# 
def handle_exit_nomouse(event): #  
    print('Exit command detected. Closing nomouse.')
    statusbar.destroy()
# 
def handle_hide_statusbar(event): #  
    statusbar.withdraw()
# 
def handle_show_statusbar(event): #  
    statusbar.deiconify()
# 
def handle_refresh_highlight(event): #  
    width, height, x_offset, y_offset, highlight_active = state['highlight']
    if highlight_active:
        highlight_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        highlight_window.deiconify()
    else:
        highlight_window.withdraw()
# 
# 
#  bind event handlers!
statusbar.bind('<<event_refresh_statusbar>>', handle_refresh_statusbar)
statusbar.bind('<<event_exit_nomouse>>', handle_exit_nomouse)
statusbar.bind('<<event_hide_statusbar>>', handle_hide_statusbar)
statusbar.bind('<<event_show_statusbar>>', handle_show_statusbar)
statusbar.bind('<<event_refresh_highlight>>', handle_refresh_highlight)
# 
# 
#  create callback functions!
#  create the functions
def get_mode(): #  
    return state['current_mode']
# 
def set_status(text): #  
    state['status_text'] = text
    statusbar.event_generate("<<event_refresh_statusbar>>")
# 
def exit_nomouse(): #  
    statusbar.event_generate("<<event_exit_nomouse>>")
# 
def set_hidden(truth): #  
    if(truth):
        statusbar.event_generate("<<event_hide_statusbar>>")
        state['statusbar_hidden']=True
    else:
        statusbar.event_generate("<<event_show_statusbar>>")
        state['statusbar_hidden']=False
# 
def highlight(highlight_props): #  
    if len(highlight_props)!=5:
        raise ValueError('highlight_props is a tuple with 5 values, width(int), height(int), x_offset(int), y_offset(int), and highlight_active(bool)')
    state['highlight'] = highlight_props
    statusbar.event_generate("<<event_refresh_highlight>>")
# 
def get_screen_resolution(): #  
    return screen_width, screen_height
# 
# 
#  put em in a dictionary!
callbacks = {'get_mode':get_mode, 'set_status':set_status, 'exit_nomouse':exit_nomouse, 'set_hidden':set_hidden, 'highlight':highlight, 'get_screen_resolution':get_screen_resolution}
# 
# 
# 
def main_loop(starting_mode='IDLE'): #  
    print(f'launching into mode {starting_mode}')
    mode = starting_mode
    state['mouse'] = Controller()
    while True:
        if mode not in mode_runners:
            print(f'mode {mode} does not appear to have a registered runner. defaulting to IDLE mode')
            mode = 'IDLE'
            raise RuntimeError()
        
        highlight((0,0,0,0,True))
        state['current_mode']=mode
        def nop():
            pass
        keyboard.unhook_all()
        statusbar.event_generate("<<event_refresh_statusbar>>")
        set_hidden(False)
        mode = mode_runners[mode](callbacks, state)
# 
#  launch the program!
#  launch main loop
Thread(target=main_loop).start()
# 
#  start gui loop!
statusbar.mainloop()
# 
# 
