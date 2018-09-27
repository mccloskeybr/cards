import pygame
import json
import main

color = {
    'white' : (255, 255, 255),
    'black' : (0, 0, 0),
    'red'   : (255, 0, 0),
    'blue'  : (0, 0, 255),
    'green' : (0, 255, 0),
    'purple': (255, 0, 255),
    'orange': (255, 127, 0)
}

card_images = None
CARD_W = 140
CARD_H = 200

class Button():
    def __init__(self, screen, x, y, w, h, idle_color, active_color, text, action=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.idle_color = idle_color
        self.active_color = active_color
        self.text = text
        self.action = action
        self.active = False

    # checks to see if the button is being clicked -- if so, do action
    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # button is active and click false
        if self.active and click[0] == 0:
            self.active = False

        # button is not active and click true
        elif not self.active \
                and click[0] == 1 \
                and self.x + self.w > mouse[0] > self.x \
                and self.y + self.h > mouse[1] > self.y:

            self.active = True
            if self.action is not None:
                self.action()

    # renders the button in the correct color
    def render(self):
        if self.active:
            pygame.draw.rect(self.screen, color[self.active_color], (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(self.screen, color[self.idle_color], (self.x, self.y, self.w, self.h))

        font = pygame.font.SysFont("Comic Sans MS", 16)
        textSurface = font.render(self.text, False, (0, 0, 0))
        self.screen.blit(textSurface, (self.x, self.y))


class Table():
    def __init__(self, screen, playerId):
        self.screen = screen
        self.playerId = playerId
        self.hands = [[], [], [], []]
        self.mainDeck = []
        self.onTable = []
        self.json = ""

    # updates the object iff the json input is different from the stored json
    def update(self, json_str):
        if self.json != json_str:
            self.json = json_str
            parsed_json = json.loads(json_str)

            for i in range(len(parsed_json['hands'])):
                self.hands[parsed_json['hands'][i]['id']] = parsed_json['hands'][i]['cards']

            self.mainDeck = parsed_json['mainDeck']
            self.onTable = parsed_json['onTable']

    # renders a given deck with x midpoint and y
    def _render_deck(self, deck, x_mid, y):
        x_spacer = 30
        full_hand_width = (len(deck) - 1) * x_spacer + CARD_W

        x = main.GAME_WIDTH/2 - full_hand_width/2
        for i in range(len(deck)):
            self.screen.blit(card_images[deck[i]], (x, y))
            x += x_spacer

    # renders all relevant decks
    def render(self):
        if card_images == None:
            load_card_imgs()

        self._render_deck(self.onTable, main.GAME_WIDTH/2, main.GAME_HEIGHT/2 - CARD_H/2)
        self._render_deck(self.hands[self.playerId], main.GAME_WIDTH/2, main.GAME_HEIGHT - CARD_H - 20)



def load_card_imgs():
    global card_images
    card_images = {}
    suits = ['spades', 'clubs', 'hearts', 'diamonds']
    for i in range(1, 14):
        for suit in suits:
            key = str(i) + ' ' + suit
            card_images[key] = pygame.image.load('./res/card_imgs/' + str(i) + '_of_' + suit + '.png');
            card_images[key] = pygame.transform.scale(card_images[key], (CARD_W, CARD_H))


