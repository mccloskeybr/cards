import pygame
import json
import main
import request
import forms

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
        self.img = pygame.transform.rotate(card_images[img_key], rot)
        self.back_img = pygame.transform.rotate(card_images['back'], rot)
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
    def check(self, show_card):
        global SELECTED_CARD
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.show = show_card

        self.render_x = self.x
        self.render_y = self.y

        # was selected and user let go of button
        # TODO: place on table or hand depending on where mouse coords are
        if SELECTED_CARD == self and click[0] == 0:
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
            self.screen.blit(self.img, (self.render_x, self.render_y))
        else:
            self.screen.blit(self.back_img, (self.render_x, self.render_y))


'''
Deck class. Manages a set of card objects.
Management includes mass checking and rendering of cards.

'''
class Deck():
    def __init__(self, screen, show, rot, x_mid, y_mid, spacer):
        self.cards = []
        self.card_keys = []
        self.screen = screen
        self.show = show
        self.rot = rot
        self.x_mid = x_mid
        self.y_mid = y_mid
        self.spacer = spacer
        self.rect = pygame.Rect(0, 0, 0, 0)

    # Updates the cards given an array of card keys (from table JSON)
    def set_cards(self, card_keys):

        # if equal lengths, do nothing
        if len(self.card_keys) == len(card_keys):
            return

        # draw horizontally if even (if rotation is 0 or 180)
        draw_horiz = ((self.rot/90) % 2 == 0)

        # if recorded key set is greater, remove a card
        if len(self.card_keys) > len(card_keys):
            i = 0
            while i < len(self.card_keys):
                if self.card_keys[i] not in card_keys:
                    self.card_keys.pop(i)
                    self.cards.pop(i)
                    i -= 1
                i += 1

        # if recorded key set is smaller, add cards
        else:
            for key in card_keys:
                if key not in self.card_keys:
                    self.card_keys.append(key)
                    self.cards.append(Card(self.screen, self, key, self.show, self.rot, draw_horiz, -1, -1, -1))

        full_deck_width = (len(self.cards) - 1) * self.spacer + CARD_W

        # if draw horizontally, the y value is constant and x value changes
        if draw_horiz:
            self.rect.x = self.x_mid - full_deck_width/2
            self.rect.y = self.y_mid
            self.rect.w = full_deck_width
            self.rect.h = CARD_H

            static_coord = self.y_mid
            variable_coord = self.x_mid - full_deck_width/2
        # if draw vertically, the x value is constant and y value changes
        else:
            self.rect.x = self.x_mid
            self.rect.y = self.y_mid - full_deck_width/2
            self.rect.w = CARD_H
            self.rect.h = full_deck_width

            static_coord = self.x_mid
            variable_coord = self.y_mid - full_deck_width/2

        # change card vars to reflect change
        for i in range(len(self.cards)):
            if draw_horiz:
                self.cards[i].x = variable_coord
                self.cards[i].y = static_coord
                if i == len(self.cards) - 1:
                    self.cards[i].click_w = CARD_W
                else:
                    self.cards[i].click_w = self.spacer

            else:
                self.cards[i].x = static_coord
                self.cards[i].y = variable_coord
                if i == len(self.cards) - 1:
                    self.cards[i].click_w = CARD_W
                else:
                    self.cards[i].click_w = self.spacer

            variable_coord += self.spacer

    # Checks all cards
    def check(self, show_hand):
        for card in self.cards:
            card.check(show_hand)

    # Renders all cards
    def render(self):
        pos = self.rot/90
        if pos == 0 or pos == 3:    
            for card in self.cards:
                card.render()
        else:
            for card in reversed(self.cards):
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
        self.json = ''
        self.players_json = ''
        self.display_names = ['', '', '', '']
        self.show_hands = [False, False, False, False]
        self.show_player_hand_toggle = False

        self.mainDeck = Deck(screen, False, 0, main.GAME_WIDTH/2 - CARD_W, main.GAME_HEIGHT/2 - CARD_H - 75, 1)
        self.discard = Deck(screen, True, 0, main.GAME_WIDTH/2 + CARD_W, main.GAME_HEIGHT/2 - CARD_H - 75, 1)
        self.onTable = Deck(screen, True, 0, main.GAME_WIDTH/2, main.GAME_HEIGHT/2 - 50, 30)
        self.hands = []
        for i in range(0, 4):
            # space between hand and edge of screen
            opponent_hand_spacer = 50

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
    def load_json(self, json_str, players_json):
        if self.json != json_str:
            self.json = json_str
            parsed_json = json.loads(json_str)

            self.mainDeck.set_cards(parsed_json['mainDeck'])
            self.discard.set_cards(parsed_json['discard'])
            self.onTable.set_cards(parsed_json['onTable'])
            for i in range(len(parsed_json['hands'])):
                self.hands[parsed_json['hands'][i]['id']].set_cards(parsed_json['hands'][i]['cards'])

        if self.players_json != players_json:
            self.players_json = players_json
            players = json.loads(players_json)['players']
            for player in players:
                self.display_names[player['id']] = player['name']
                self.show_hands[player['id']] = (player['showHand'] == 'True')

    # checks all relevant decks. also handles when a selected card is unselected.
    def check(self):
        global SELECTED_CARD
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # show hand
        if (click[2] == 1 and self.show_player_hand_toggle == False and self.hands[self.player_id].rect.collidepoint(mouse)) or \
                (click[2] == 0 and self.show_player_hand_toggle == True) :

            self.show_player_hand_toggle = not self.show_player_hand_toggle
            request.toggle_show_hand(self.player_id)

        # capture letting go of card before its passed to decks
        if click[0] == 0 and SELECTED_CARD != None:
            dist_to_main    = ((mouse[0] - self.mainDeck.x_mid)**2 + (mouse[1] - self.mainDeck.y_mid - CARD_H/2)**2)**(0.5)
            dist_to_discard = ((mouse[0] - self.discard.x_mid)**2 + (mouse[1] - self.discard.y_mid - CARD_H/2)**2)**(0.5)
            dist_to_table   = ((mouse[0] - self.onTable.x_mid)**2 + (mouse[1] - self.onTable.y_mid - CARD_H/2)**2)**(0.5)
            dist_to_hand    = ((mouse[0] - self.hands[self.player_id].x_mid)**2 + (mouse[1] - self.hands[self.player_id].y_mid - CARD_H/2)**2)**(0.5)

            if SELECTED_CARD.deck == self.mainDeck:
                if dist_to_table < dist_to_main and dist_to_table < dist_to_hand:
                    request.draw_main_to_table()
                elif dist_to_hand < dist_to_main and dist_to_hand < dist_to_table:
                    request.draw_main_to_hand(self.player_id)

            elif SELECTED_CARD.deck == self.discard:
                if dist_to_hand < dist_to_table and dist_to_hand < dist_to_discard:
                    request.draw_discard_to_hand(self.player_id)
                elif dist_to_table < dist_to_hand and dist_to_table < dist_to_discard:
                    request.draw_discard_to_table()

            elif SELECTED_CARD.deck == self.onTable:
                if dist_to_hand < dist_to_table and dist_to_hand < dist_to_discard:
                    request.draw_table_to_hand(self.player_id, self.onTable.cards.index(SELECTED_CARD))
                elif dist_to_discard < dist_to_hand and dist_to_discard < dist_to_table:
                    request.draw_table_to_discard(self.onTable.cards.index(SELECTED_CARD))

            elif SELECTED_CARD.deck == self.hands[self.player_id]:
                if dist_to_table < dist_to_hand and dist_to_table < dist_to_discard:
                    request.draw_hand_to_table(self.player_id, self.hands[self.player_id].cards.index(SELECTED_CARD))
                elif dist_to_discard < dist_to_hand and dist_to_discard < dist_to_table:
                    request.draw_hand_to_discard(self.player_id, self.hands[self.player_id].cards.index(SELECTED_CARD))

        # tell decks to check status of their cards
        self.mainDeck.check(False)
        self.discard.check(True)
        self.onTable.check(True)
        for index, hand in enumerate(self.hands):
            # backwards from the perspective of the player
            if index == self.player_id:
                hand.check(not self.show_hands[index])
            else:
                hand.check(self.show_hands[index])

    # renders all relevant decks
    def render(self):
        global SELECTED_CARD
        
        self.mainDeck.render()
        self.discard.render()
        self.onTable.render()
        for hand in self.hands:
            hand.render()
    
        # render display names if hover
        mouse = pygame.mouse.get_pos()
        for index, hand in enumerate(self.hands):
            if index == self.player_id:
                continue

            if hand.rect.collidepoint(mouse):
                name = self.display_names[index]

                text_font = pygame.font.SysFont('Comic Sans MS', 16)
                text_surface = text_font.render(name, True, forms.colors['white'])

                w, h = text_font.size(name)
                x = mouse[0] - w/2
                y = mouse[1] - h
                if x < 0:
                    x = 0
                elif x + w > main.GAME_WIDTH:
                    x -= x + w - main.GAME_WIDTH

                if y < 0:
                    y = 0
                elif y + h > main.GAME_HEIGHT:
                    y -= y + h - main.GAME_HEIGHT

                pygame.draw.rect(self.screen, forms.colors['gray'], (x, y, w, h))
                self.screen.blit(text_surface, (x, y))

        # ensure selected card is rendered on top
        if SELECTED_CARD != None:
            SELECTED_CARD.render()


