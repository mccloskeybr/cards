
from ctypes import *

'''
Python file for interfacing the backend
'''

_library = CDLL('./cards_backend.so')

class Card(Structure): pass
Card._fields_ = [
    ('suit', c_int),
    ('rank', c_uint8)]

class Deck(Structure): pass
Deck._fields_ = [
    ('cards', POINTER(POINTER(Card))),
    ('rank', c_uint8)]

class Table(Structure): pass
Table._fields_ = [
    ('mainDeck', POINTER(Deck)),
    ('onTable', POINTER(Deck)),
    ('hands', POINTER(POINTER(Deck)))]

# table.c functions
_library.construct_table.argtypes       = [c_uint8]
_library.construct_table.restype        = POINTER(Table)

_library.reset_table.argtypes           = [POINTER(Table)]
_library.reset_table.restype            = None

_library.draw_main_to_table.argtypes    = [POINTER(Table)]
_library.draw_main_to_table.restype     = c_bool

_library.draw_main_to_hand.argtypes     = [POINTER(Table), c_uint8]
_library.draw_main_to_hand.restype      = c_bool

_library.draw_hand_to_table.argtypes    = [POINTER(Table), c_uint8, c_uint8]
_library.draw_hand_to_table.restype     = c_bool

_library.draw_table_to_hand.argteyps    = [POINTER(Table), c_uint8, c_uint8]
_library.draw_table_to_hand.restype     = c_bool

# cards.c functions
_library.shuffle.argtypes               = [POINTER(Deck)]
_library.shuffle.restype                = None

_library.print_deck.argtypes            = [POINTER(Deck)]
_library.print_deck.restype             = None

# wrapper/interfacing functions

class TableWrapperClass(object):

    # initializes a table
    def __init__(self, numHands):
        self.table = _library.construct_table(c_uint8(numHands))

    # resets the table
    def reset_table(self):
        _library.reset_table(self.table)

    # shuffles the main deck
    def shuffle_main_deck(self):
        _library.shuffle(self.table.contents.mainDeck)

    # draws a single card from the main deck to the table
    def draw_main_to_table(self):
        return bool(_library.draw_main_to_table(self.table))

    # draws a single card from the main deck to a hand
    def draw_main_to_hand(self, hand_index):
        return bool(_library.draw_main_to_hand(self.table, c_uint8(hand_index)))

    # places a card from a hand onto the table
    def draw_hand_to_table(self, hand_index, card_index):
        return bool(_library.draw_hand_to_table(self.table, c_uint8(hand_index), c_uint8(card_index)))

    # places a card from the table into a hand
    def draw_table_to_hand(self, hand_index, card_index):
        return bool(_library.draw_table_to_hand(self.table, c_uint8(hand_index), c_uint8(card_index)))

    def print_main(self):
        _library.print_deck(self.table.contents.mainDeck)


