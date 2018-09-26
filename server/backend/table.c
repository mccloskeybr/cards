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
 */
extern __declspec(dllexport) void destroy_table() {
    destroy_cards_in_deck(TABLE->mainDeck);
    destroy_deck(TABLE->mainDeck);
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
void reset_table() {
    uint8_t numHands = TABLE->numHands;

    destroy_table(TABLE);
    construct_table(numHands);
}

/**
 * shuffles the main deck of the TABLE
 */
void shuffle_main() {
    shuffle(TABLE->mainDeck);
    print_deck(TABLE->mainDeck);

    char * test = calloc(1000, sizeof(char));
    get_table_json(test);
    free(test);
}

/** ---------------- UTILITY ---------------- **/

/**
 * Places a card onto the main TABLE/playing frield from the main deck
 */
bool draw_main_to_table() {

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
bool draw_main_to_hand(uint8_t index) {

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
bool draw_hand_to_table(uint8_t hand_index, uint8_t card_index) {

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
bool draw_table_to_hand(uint8_t hand_index, uint8_t card_index) {

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


extern __declspec(dllexport) void get_table_json(char * buff) {
    char * tempBuff = calloc(100, sizeof(char));

    strcat(buff, "{");

    sprintf(tempBuff, "\"numHands\" : %d,", TABLE->numHands);
    strcat(buff, tempBuff);

    sprintf(tempBuff, "\"mainDeck\" : [");
    strcat(buff, tempBuff);
    int i;
    for (i = 0; i <= TABLE->mainDeck->currCard; i++) {
        
        Card * currCard = TABLE->mainDeck->cards[i];
        sprintf(tempBuff, "%d ", currCard->rank);
        strcpy(buff, tempBuff);
        //suit_to_string(currCard, buff);

        if (i != TABLE->mainDeck->currCard) {
            strcat(buff, ",");
        }
    }

    strcat(buff, "}");
    printf(buff);
}



