#include "table.h"

const char table_classname[] = "table.c";

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

    return table;

}

void destroy_table(struct Table * toFree) {
    destroy_cards_in_deck(toFree->mainDeck);
    destroy_deck(toFree->mainDeck);
    destroy_deck(toFree->onTable);

    int i;
    for (i = 0; i < toFree->numHands; i++) {
        destroy_deck(toFree->hands[i]);
    }

    free(toFree->hands);
}
