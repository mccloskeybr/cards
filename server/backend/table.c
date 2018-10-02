#include <string.h>
#include "table.h"

const char TABLE_classname[] = "table.c";

Table * TABLE;

/** ---------------- CON/DESTUCTORS ---------------- **/

/**
 * Generates a TABLE struct
 */
extern __declspec(dllexport) void construct_table(uint8_t numHands) {

    TABLE = malloc(sizeof(Table));
    TABLE->mainDeck = construct_std_deck();
    TABLE->discard = construct_deck(TABLE->mainDeck->maxCards);
    TABLE->onTable = construct_deck(TABLE->mainDeck->maxCards);
    TABLE->hands = malloc(numHands * sizeof(Deck *));
    TABLE->numHands = numHands;

    uint8_t i;
    for (i = 0; i < numHands; i++) {
        TABLE->hands[i] = construct_deck(TABLE->mainDeck->maxCards);
    }

    write_to_log(TABLE_classname, "Constructed the TABLE successfully.");

}


/**
 * Destroyes a TABLE struct
 * (including all decks and relative cards)
 *
 * CARD references are stored in the MAINDECK, so only need
 * to destroy the cards there. Destroying cards in other decks
 * will cause double free.
 */
extern __declspec(dllexport) void destroy_table() {
    destroy_cards_in_deck(TABLE->mainDeck);
    destroy_deck(TABLE->mainDeck);
    destroy_deck(TABLE->discard);
    destroy_deck(TABLE->onTable);

    int i;
    for (i = 0; i < TABLE->numHands; i++) {
        destroy_deck(TABLE->hands[i]);
    }

    free(TABLE->hands);
    free(TABLE);

    write_to_log(TABLE_classname, "Destroyed the TABLE successfully.");
}


/**
 * Resets the TABLE by freeing and constructing a new TABLE
 */
extern __declspec(dllexport) void reset_table() {
    uint8_t numHands = TABLE->numHands;

    destroy_table(TABLE);
    construct_table(numHands);
}

/**
 * shuffles the main deck of the TABLE
 */
extern __declspec(dllexport) void shuffle_main() {
    shuffle(TABLE->mainDeck);
}

/** ---------------- UTILITY ---------------- **/

/**
 * Places a card onto the main TABLE/playing frield from the main deck
 */
extern __declspec(dllexport) bool draw_main_to_table() {

    // attempt to draw the card. if fail, stop
    Card * card = draw_card(TABLE->mainDeck);
    if (card == NULL) {
        return false;
    }

    // attempt to place the card onto relevant deck. if fail,
    // place back in original deck (should succeed every time
    // because we just drew from that deck) and return false
    if(!place_card(TABLE->onTable, card)) {
        place_card(TABLE->mainDeck, card);
        return false;
    }

    // succeeded
    return true;

}

/**
 * Places a card from the main deck into one of the hands
 */
extern __declspec(dllexport) bool draw_main_to_hand(uint8_t index) {

    Card * card = draw_card(TABLE->mainDeck);
    if (card == NULL) {
        return false;
    }

    if(!place_card(TABLE->hands[index], card)) {
        place_card(TABLE->mainDeck, card);
        return false;
    }

    return true;

}

/**
 * Places a card onto the TABLE from one of the hands
 */
extern __declspec(dllexport) bool draw_hand_to_table(uint8_t hand_index, uint8_t card_index) {

    Card * card = draw_specific_card(TABLE->hands[hand_index], card_index);
    if (card == NULL) {
        return false;
    }

    if(!place_card(TABLE->onTable, card)) {
        place_card(TABLE->hands[hand_index], card);
        return false;
    }

    return true;

}

/**
 * Places a card onto a specified hand from the TABLE
 */
extern __declspec(dllexport) bool draw_table_to_hand(uint8_t hand_index, uint8_t card_index) {

    Card * card = draw_specific_card(TABLE->onTable, card_index);
    if (card == NULL) {
        return false;
    }

    if(!place_card(TABLE->hands[hand_index], card)) {
        place_card(TABLE->onTable, card);
        return false;
    }

    return true;

}

/**
 * Places a specified card from the TABLE to the discard pile
 */
extern __declspec(dllexport) bool draw_table_to_discard(uint8_t index) {

    Card * card = draw_card(TABLE->onTable);
    if (card == NULL) {
        return false;
    }

    if(!place_card(TABLE->discard, card)) {
        place_card(TABLE->onTable, card);
        return false;
    }

    return true;
}


/**
 * Places a card from a specified hand into the discard pile
 */
extern __declspec(dllexport) bool draw_hand_to_discard(uint8_t hand_index, uint8_t card_index) {

    Card * card = draw_specific_card(TABLE->hands[hand_index], card_index);
    if (card == NULL) {
        return false;
    }

    if(!place_card(TABLE->discard, card)) {
        place_card(TABLE->hands[hand_index], card);
        return false;
    }

    return true;
}

/**
 * Creates a deck json, starting from [
 * e.g. [ "12 hearts, 13 clubs, ... ]
 */
void put_deck_json(char * buff, Deck * deck) {
    char * tempBuff = calloc(20, sizeof(char));

    strcat(buff, "[");

    int i;
    for (i = 0; i <= deck->currCard; i++) {
        
        Card * currCard = deck->cards[i];
        sprintf(tempBuff, "\"%d ", currCard->rank);
        switch(currCard->suit) {
            case hearts:
                strcat(tempBuff, "hearts");
                break;
            case diamonds:
                strcat(tempBuff, "diamonds");
                break;
            case spades:
                strcat(tempBuff, "spades");
                break;
            case clubs:
                strcat(tempBuff, "clubs");
                break;
            default:
                strcat(tempBuff, "ERR");
                break;
        }
        strcat(tempBuff, "\"");

        if (i != deck->currCard) {
            strcat(tempBuff, ",");
        }
        strcat(buff, tempBuff);
    }

    strcat(buff, "]");

    free(tempBuff);
}

/**
 * Creates a table json with information of all decks
 */
extern __declspec(dllexport) void put_table_json(char * buff) {
    char * tempBuff = calloc(30, sizeof(char));

    strcat(buff, "{");

    sprintf(tempBuff, "\"numHands\" : %d,", TABLE->numHands);
    strcat(buff, tempBuff);

    strcat(buff, "\"mainDeck\" : ");
    put_deck_json(buff, TABLE->mainDeck);
    strcat(buff, ",");

    strcat(buff, "\"discard\" : ");
    put_deck_json(buff, TABLE->discard);
    strcat(buff, ",");

    strcat(buff, "\"onTable\" : ");
    put_deck_json(buff, TABLE->onTable);
    strcat(buff, ",");


    strcat(buff, "\"hands\": [");
    int i;
    for (i = 0; i < TABLE->numHands; i++) {
        sprintf(tempBuff, "{\"id\" : %d, \"cards\" :", i);
        strcat(buff, tempBuff);
        put_deck_json(buff, TABLE->hands[i]);
        strcat(buff, "}");

        if (i != TABLE->numHands - 1) {
            strcat(buff, ",");
        }
    }
    strcat(buff, "]");

    strcat(buff, "}");
    printf(buff);

    free(tempBuff);
}



