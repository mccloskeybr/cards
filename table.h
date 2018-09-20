#include "log.h"
#include "cards.h"

#ifndef __TABLE_H
#define __TABLE_H

struct Table {
    struct Deck * mainDeck;
    struct Deck * onTable;
    struct Deck ** hands;
    uint8_t numHands;
};

struct Table * construct_table(uint8_t numHands);
void destroy_table(struct Table * toFree);

#endif //table.h
