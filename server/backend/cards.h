#ifndef __CARDS_H
#define __CARDS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
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
typedef struct {
    enum Suit suit;
    uint8_t rank;
} Card;

/**
 * Represents a deck objects (a collection of 52 cards)
 *
 * Decks are treated like stacks:
 *  The currCard is the top of the stack, with bottom being
 *  currCard = 0 and top currCard = maxCards
**/
typedef struct {
    Card ** cards;
    int8_t currCard;
    int8_t maxCards;
} Deck;




//------------- FUNCTIONS --------------

Card * construct_card(enum Suit suit, uint8_t rank);
void destroy_card(Card * toFree);
Deck * construct_deck(int8_t maxCards);
Deck * construct_std_deck();
void destroy_deck(Deck * toFree);
void destroy_cards_in_deck(Deck * deck);

extern __declspec(dllexport) void shuffle(Deck * deck);

Card * draw_card(Deck * deck);
Card * draw_specific_card(Deck * deck, uint8_t card_index);
bool place_card(Deck * deck, Card * card);

void suit_to_string(Card * card, char * buff);
void print_card(Card * toPrint);
void print_deck(Deck * toPrint);

#endif //cards.h
