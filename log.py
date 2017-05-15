import libtcodpy
import textwrap
import config


def init():
    global game_messages

    game_messages = []


def add_message(message, color=libtcodpy.white):
    global game_messages
    message_lines = textwrap.wrap(message, config.MSG_WIDTH)

    for line in message_lines:
        if len(game_messages) == config.MSG_HEIGHT:
            del game_messages[0]

        game_messages.append((line, color))