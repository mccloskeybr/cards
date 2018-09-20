#ifndef __CARDS_H
#define __CARDS_H

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "log.h"

#define NUMCARDS 52

//------------- STRUCTS -------------


/**
 * Enum for each available suit
**/
enum Suit {
    spades = 0,
    clubs = 1,
    hearts = 2,
    diamonds = 3
};

/**
 * Represents a single card
 * Owns:
 *  name
 *  suit
 *  rank
**/
struct Card {
    enum Suit suit;
    uint8_t rank;
};

/**
 * Represents a deck objects (a collection of 52 cards)
 *
 * Decks are treated like stacks:
 *  The currCard is the top of the stack, with bottom being
 *  currCard = 0 and top currCard = maxCards
**/
struct Deck {
    struct Card ** cards;
    int8_t currCard;
    int8_t maxCards;
};




//------------- FUNCTIONS --------------

struct Card * construct_card(enum Suit suit, uint8_t rank);
void destroy_card(struct Card * toFree);
struct Deck * construct_deck(int8_t maxCards);
struct Deck * construct_std_deck();
void destroy_deck(struct Deck * toFree);
void destroy_cards_in_deck(struct Deck * deck);

void shuffle(struct Deck * deck);
struct Card * draw_card(struct Deck * deck);
struct Card * place_card(struct Deck * deck, struct Card * card);

void suit_to_string(struct Card * card, char * buff);
void print_card(struct Card * toPrint);
void print_deck(struct Deck * toPrint);

#endif //cards.h
