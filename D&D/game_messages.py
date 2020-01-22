# import textwrap

import tcod


class Message(object):
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
