#include <stdbool.h>
#include "log.h"
#include "cards.h"

#ifndef __TABLE_H
#define __TABLE_H

//------------- STRUCTS ------------- 


/**
 * Represents all relevant decks to the table
 * Owns:
 *  the main deck (the source of ALL cards rooted here, be careful not to double free)
 *  the cards shown on the table
 *  all of the hands of the players
 */
struct Table {
    struct Deck * mainDeck;
    struct Deck * onTable;
    struct Deck ** hands;
    uint8_t numHands;
};



//------------- FUNCTIONS ------------- 

struct Table * construct_table(uint8_t numHands);
void destroy_table(struct Table * toFree);

void reset_table(struct Table * table);

bool draw_main_to_table(struct Table * table);
bool draw_main_to_hand(struct Table * table, uint8_t index);
bool draw_hand_to_table(struct Table * table, uint8_t hand_index, uint8_t card_index);
bool draw_table_to_hand(struct Table * table, uint8_t hand_index, uint8_t card_index);

#endif //table.h
