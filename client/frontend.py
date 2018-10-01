import pygame
import json
import main
import request

CARD_W = 140
CARD_H = 200

SELECTED_CARD = None    # the current card being dragged around

# loads all relevant card images
card_images = {}
card_images['back'] = pygame.transform.scale(pygame.image.load('./res/card_imgs/back.png'), (CARD_W, CARD_H))
suits = ['spades', 'clubs', 'hearts', 'diamonds']
for i in range(1, 14):
    for suit in suits:
        key = str(i) + ' ' + suit
        card_images[key] = pygame.image.load('./res/card_imgs/' + str(i) + '_of_' + suit + '.png')
        card_images[key] = pygame.transform.scale(card_images[key], (CARD_W, CARD_H))


'''
Class representing a single card. Keeps track of all rendering AND
selection information -- when a card is clicked, this class captures that
action.

'''
class Card():
    def __init__(self, screen, deck, img_key, show, rot, draw_horiz, x, y, click_w):
        self.screen = screen
        self.deck = deck
        self.img = card_images[img_key]
        self.back_img = card_images['back']
        self.show = show
        self.rot = rot

        # location specifics of card in relation to rest of deck
        self.x = x
        self.y = y
        self.w = CARD_W
        self.h = CARD_H

        # render specifics of card -- if card is clicked and dragged
        self.render_x = self.x
        self.render_y = self.y
        if draw_horiz:              # click box of card diff depending on orientation
            self.click_w = click_w
            self.click_h = self.h   
        else:
            self.click_w = self.w
            self.click_h = click_w

    # checks to see if the card has been selected. if so, have card follow mouse
    def check(self):
        global SELECTED_CARD
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # was selected and user let go of button
        # TODO: place on table or hand depending on where mouse coords are
        if SELECTED_CARD == self and click[0] == 0:
            self.render_x = self.x
            self.render_y = self.y
            SELECTED_CARD = None

        # user is currently dragging the card
        elif SELECTED_CARD == self and click[0] == 1:
            self.render_x = mouse[0] - self.w / 2
            self.render_y = mouse[1] - self.h / 2

        # user clicks the card
        elif SELECTED_CARD == None and click[0] == 1 and SELECTED_CARD == None \
                and self.x < mouse[0] < self.x + self.click_w \
                and self.y < mouse[1] < self.y + self.click_h:
            SELECTED_CARD = self

    # renders the card
    def render(self):
        if self.show:
            self.screen.blit(pygame.transform.rotate(self.img, self.rot), (self.render_x, self.render_y))
        else:
            self.screen.blit(pygame.transform.rotate(self.back_img, self.rot), (self.render_x, self.render_y))


'''
Deck class. Manages a set of card objects.
Management includes mass checking and rendering of cards.

'''
class Deck():
    def __init__(self, screen, show, rot, x_mid, y_mid, spacer):
        self.cards = []
        self.screen = screen
        self.show = show
        self.rot = rot
        self.x_mid = x_mid
        self.y_mid = y_mid
        self.spacer = spacer

    # Updates the cards given an array of card keys (from table JSON)
    def set_cards(self, cards):
        self.cards = [] #TODO: Make more efficient

        full_deck_width = (len(cards) - 1) * self.spacer + CARD_W
        
        # draw horizontally if even (if rotation is 0 or 180)
        draw_horiz = ((self.rot/90) % 2 == 0)

        # if draw horizontally, the y value is constant and x value changes
        if draw_horiz:
            static_coord = self.y_mid
            variable_coord = self.x_mid - full_deck_width/2
        # if draw vertically, the x value is constant and y value changes
        else:
            static_coord = self.x_mid
            variable_coord = self.y_mid - full_deck_width/2

        for i in range(len(cards)):
            card_key = cards[i]
            if draw_horiz:
                if i == len(cards) - 1:
                    self.cards.append(Card(self.screen, self, card_key, self.show, self.rot, True, variable_coord, static_coord, CARD_W))
                else:
                    self.cards.append(Card(self.screen, self, card_key, self.show, self.rot, True, variable_coord, static_coord, self.spacer)) 

            else:
                if i == len(cards) - 1:
                    self.cards.append(Card(self.screen, self, card_key, self.show, self.rot, False, static_coord, variable_coord, CARD_W))
                else:
                    self.cards.append(Card(self.screen, self, card_key, self.show, self.rot, False, static_coord, variable_coord, self.spacer))

            variable_coord += self.spacer

    # Checks all cards
    def check(self):
        for card in self.cards:
            card.check()

    # Renders all cards
    def render(self):
        for card in self.cards:
            card.render()


'''
Table class. Keeps track of relevant deck objects.
Hands are kept consistent (in circular shape around table) via. player_id (given from server).
Deck objects are updated via. json object retrieved from server.

'''
class Table():
    def __init__(self, screen, player_id):
        self.screen = screen
        self.player_id = player_id
        self.json = ""

        self.mainDeck = Deck(screen, False, 0, main.GAME_WIDTH/2, main.GAME_HEIGHT/2 - CARD_H - 75, 5)
        self.onTable = Deck(screen, True, 0, main.GAME_WIDTH/2, main.GAME_HEIGHT/2 - 50, 30)
        self.hands = []
        for i in range(0, 4):
            # space between hand and edge of screen
            opponent_hand_spacer = 40

            # following checks ensure circular positioning of hands around table
            pos = (i - self.player_id) % 4
            if pos == 0:
                self.hands.append(Deck(screen, True, 0, main.GAME_WIDTH/2, main.GAME_HEIGHT - CARD_H - 10, 30))
            elif pos == 1:
                self.hands.append(Deck(screen, False, 90, main.GAME_WIDTH - opponent_hand_spacer, main.GAME_HEIGHT / 2, 30))
            elif pos == 2:
                self.hands.append(Deck(screen, False, 180, main.GAME_WIDTH/2, -CARD_H + opponent_hand_spacer, 30))
            elif pos == 3:
                self.hands.append(Deck(screen, False, 270, -CARD_H + opponent_hand_spacer, main.GAME_HEIGHT/2, 30))

    # updates the object iff the json input is different from the stored json
    def load_json(self, json_str):
        if self.json != json_str:
            self.json = json_str
            parsed_json = json.loads(json_str)

            self.mainDeck.set_cards(parsed_json['mainDeck'])
            self.onTable.set_cards(parsed_json['onTable'])
            for i in range(len(parsed_json['hands'])):
                self.hands[parsed_json['hands'][i]['id']].set_cards(parsed_json['hands'][i]['cards'])

    # checks all relevant decks. also handles when a selected card is unselected.
    def check(self):
        global SELECTED_CARD
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # capture letting go of card before its passed to decks
        if click[0] == 0 and SELECTED_CARD != None:
            dist_to_table = ((mouse[0] - self.onTable.x_mid)**2 + (mouse[1] - self.onTable.y_mid)**2)**(0.5)
            dist_to_hand  = ((mouse[0] - self.hands[self.player_id].x_mid)**2 + (mouse[1] - self.hands[self.player_id].y_mid)**2)**(0.5)

            if dist_to_table < dist_to_hand and SELECTED_CARD.deck == self.hands[self.player_id]:
                request.draw_hand_to_table(self.player_id, self.hands[self.player_id].cards.index(SELECTED_CARD))

            elif dist_to_table > dist_to_hand and SELECTED_CARD.deck == self.onTable:
                request.draw_table_to_hand(self.player_id, self.onTable.cards.index(SELECTED_CARD))

        # tell decks to check status of their cards
        self.onTable.check()
        self.hands[self.player_id].check()

    # renders all relevant decks
    def render(self):
        global SELECTED_CARD
        
        self.mainDeck.render()
        self.onTable.render()
        for hand in self.hands:
            hand.render()

        # ensure selected card is rendered on top
        if SELECTED_CARD != None:
            SELECTED_CARD.render()


