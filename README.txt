Hi! Hannah here!

This is my program for mouse emulation. It follows a similar layout to the mouseless and mousemaster programs which inspired it.

The program has 4 modes
IDLE
CLICK
MOVE
ALTTAB

IDLE is the normal mode, it does nothing until you press alt. When alt is pressed it switches you to CLICK mode.

CLICK mode is where you select where to move. use the letter keys and ',./;' to determine where to move your cursor. There is an interactive highlighting to help you out!

When you have the position you want, press space to click or shift to right click or alt to just move there. You can press ' to start a drag. This will open you up to click mode again to select where to end the drag. Simply select a location and hit space as normal and it will end the drag.

MOVE mode is for fine details. To access move mode from IDLE mode hit alt then hold alt! MOVE mode only stays active untill you let go of alt

MOVE mode has the following hotkeys
j - move down
k - move up
l - move right
h - move left
space - left mouse button
f - right mouse button
r - hold the alt key until MOVE mode is accessed again
q - exit the program

ALTTAB mode makes sure alt+tab works exactly as you expect! no suprises here!

Example key combos:
    <alt>by<space> - click near the right side of the screen
    <alt>ttc - click the corner of the screen (closes windows!)
    <alt>,,<shift> - right click near the bottom of the screen!
    <alt>te'tq<space> - draw a window to the left!
    <alt><alt+q> - quit
    <alt><alt+r> - hold alt
    <alt><alt> - stop holding alt

#Feature request: add some ways to bind and mark specific places on the screen?
#Feature request: switch system to pynput because apparently keyboard (the library) does not suppress on linux and we already have pynput as a dependency
#Feature request: linux support! PLEASE just switch it from keyboard to pynput! IS THAT SO HARD???
> yup! yes it is.

It is a wonderful day! Bye!
Hannah Nelson
