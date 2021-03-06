#include <string.h>
#include "cards.h"
#include "log.h"

const char cards_filename[] = "cards.c";

/** ---------------- CON/DESTUCTORS ---------------- **/

/**
 * Generates a card given the suit and rank
 */
Card * construct_card(enum Suit suit, uint8_t rank) {

    Card * card = malloc(sizeof(Card));

    card->suit = suit;
    card->rank = rank;

    write_to_log(cards_filename, "Constructed a card successfully.");

    return card;

}

/**
 * Frees a card struct
 */
void destroy_card(Card * toFree) {

    free(toFree);

    write_to_log(cards_filename, "Destroyed a card successfully.");

}

/**
 * Generates a non-shuffled deck of size NUMCARDS (default)
 */
Deck * construct_deck(int8_t maxCards) {

    Deck * deck = malloc(sizeof(Deck));

    deck->currCard = -1;
    deck->maxCards = maxCards;
    deck->cards = malloc(deck->maxCards * sizeof(Card *));

    write_to_log(cards_filename, "Constructed a deck successfully.");

    return deck;

}

/**
 * makes a standard french playing card set
 */
Deck * construct_std_deck() {

    Deck * deck = construct_deck(52);

    enum Suit currSuit = 0;
    int8_t i;
    for (i = 0; i < deck->maxCards; i++) {
        place_card(deck, construct_card(currSuit, (i % 13) + 1));
        
        if (i % 13 == 12) {
            currSuit++;
        }

    }

    return deck;

}

/**
 * Frees a deck struct
 */
void destroy_deck(Deck * toFree) {

    free(toFree->cards);
    free(toFree);

    write_to_log(cards_filename, "Destroyed a deck successfully.");

}

/**
 * Frees all of the cards in the deck
 * DOES NOT FREE DECK
 */
void destroy_cards_in_deck(Deck * deck) {
    int8_t i;
    for (i = 0; i < deck->maxCards; i++) {
        destroy_card(deck->cards[i]);
    }
}


/** ---------------- UTILITY ---------------- **/

/**
 * Shuffles the deck randomly
 */
void shuffle(Deck * deck) {

    srand(time(NULL));
    int8_t i;
    for (i = 0; i < deck->currCard; i++) {
        int r = rand() % (deck->currCard + 1); //+1 because currCard is index

        Card * temp = deck->cards[r];
        deck->cards[r] = deck->cards[i];
        deck->cards[i] = temp;
    }

}

/**
 * Draws the topmost card on the deck
 * returns null on failure and card on success
 */
Card * draw_card(Deck * deck) {
    
    if (deck->currCard == -1) {
        return NULL;
    }

    return deck->cards[deck->currCard--];
}

/**
 * Draws a specific card given the index of that card in the deck
 * returns null on failure and card on success
 */
Card * draw_specific_card(Deck * deck, uint8_t index) {

    if (deck->currCard < index) {
        return NULL;
    }

    Card * card = deck->cards[index];

    //swap card with one that is in play
    deck->cards[index] = deck->cards[deck->currCard];
    deck->cards[deck->currCard] = card;
    deck->currCard--;

    return card;

}

/**
 * places card into deck
 * returns true on successful placing
 */
bool place_card(Deck * deck, Card * card) {
    if (deck->currCard >= deck->maxCards) {
        return false;
    }

    deck->cards[++deck->currCard] = card;
    return true;
}



/** ---------------- OUTPUT ---------------- **/

/**
 * Puts the string version of the Suit enum
 */
void suit_to_string(Card * card, char * buff) {

    switch(card->suit) {
        case spades:
            strcpy(buff, "Spades");
            break;
        case clubs:
            strcpy(buff, "Clubs");
            break;
        case hearts:
            strcpy(buff, "Hearts");
            break;
        case diamonds:
            strcpy(buff, "Diamonds");
            break;
        default:
            strcpy(buff, "ERR: Unexpected enum");
            break;
    }

}

/**
 * Prints the rank and suit of input card
 * i.e.
 *  2 of Diamonds
 */
void print_card(Card * toPrint) {

    char * suit_string = (char *) calloc(100, sizeof(char));
    suit_to_string(toPrint, suit_string);

    printf("%d of %s\n", toPrint->rank, suit_string);

    free(suit_string);

}

/**
 * Prints all of the non played cards in the deck
 */
void print_deck(Deck * toPrint) {

    int8_t i;
    for (i = 0; i <= toPrint->currCard; i++) {
        printf("[%d]: ", i);
        print_card(toPrint->cards[i]);
    }

    printf("--\n\n");

}

