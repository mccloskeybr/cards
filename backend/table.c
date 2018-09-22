#include "table.h"

const char table_classname[] = "table.c";

/** ---------------- CON/DESTUCTORS ---------------- **/

/**
 * Generates a table struct
 */
struct Table * construct_table(uint8_t numHands) {

    struct Table * table = malloc(sizeof(struct Table));
    table->mainDeck = construct_std_deck();
    table->onTable = construct_deck(table->mainDeck->maxCards);
    table->hands = malloc(numHands * sizeof(struct Deck *));
    table->numHands = numHands;

    uint8_t i;
    for (i = 0; i < numHands; i++) {
        table->hands[i] = construct_deck(table->mainDeck->maxCards);
    }

    //write_to_log(table_classname, "Constructed a table successfully.");

    return table;

}


/**
 * Destroyes a table struct
 * (including all decks and relative cards)
 */
void destroy_table(struct Table * toFree) {
    destroy_cards_in_deck(toFree->mainDeck);
    destroy_deck(toFree->mainDeck);
    destroy_deck(toFree->onTable);

    int i;
    for (i = 0; i < toFree->numHands; i++) {
        destroy_deck(toFree->hands[i]);
    }

    free(toFree->hands);
    free(toFree);

    write_to_log(table_classname, "Destroyed a table successfully.");
}


/**
 * Resets the table by freeing and constructing a new table
 */
void reset_table(struct Table * table) {
    uint8_t numHands = table->numHands;

    destroy_table(table);
    table = construct_table(numHands);
}

/** ---------------- UTILITY ---------------- **/

/**
 * Places a card onto the main table/playing frield from the main deck
 */
bool draw_main_to_table(struct Table * table) {

    // attempt to draw the card. if fail, stop
    struct Card * card = draw_card(table->mainDeck);
    if (card == NULL) {
        return false;
    }

    // attempt to place the card onto relevant deck. if fail,
    // place back in original deck (should succeed every time
    // because we just drew from that deck) and return false
    if(!place_card(table->onTable, card)) {
        place_card(table->mainDeck, card);
        return false;
    }

    // succeeded
    return true;

}

/**
 * Places a card from the main deck into one of the hands
 */
bool draw_main_to_hand(struct Table * table, uint8_t index) {

    struct Card * card = draw_card(table->mainDeck);
    if (card == NULL) {
        return false;
    }

    if(!place_card(table->hands[index], card)) {
        place_card(table->mainDeck, card);
        return false;
    }

    return true;

}

/**
 * Places a card onto the table from one of the hands
 */
bool draw_hand_to_table(struct Table * table, uint8_t hand_index, uint8_t card_index) {

    struct Card * card = draw_specific_card(table->hands[hand_index], card_index);
    if (card == NULL) {
        return false;
    }

    if(!place_card(table->onTable, card)) {
        place_card(table->hands[hand_index], card);
        return false;
    }

    return true;

}

/**
 * Places a card onto a specified hand from the table
 */
bool draw_table_to_hand(struct Table * table, uint8_t hand_index, uint8_t card_index) {

    struct Card * card = draw_specific_card(table->onTable, card_index);
    if (card == NULL) {
        return false;
    }

    if(!place_card(table->hands[hand_index], card)) {
        place_card(table->onTable, card);
        return false;
    }

    return true;

}



