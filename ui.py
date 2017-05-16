"""
    Check for keyboard and mouse events. Call init() before use, poll() to update, and use
    ui.key and ui.mouse to access data
"""

import libtcodpy


def init():
    global key, mouse
    mouse = libtcodpy.Mouse()
    key = libtcodpy.Key()


def poll():
    libtcodpy.sys_check_for_event(libtcodpy.EVENT_KEY_PRESS|libtcodpy.EVENT_MOUSE, key, mouse)
