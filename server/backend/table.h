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
typedef struct {
    Deck * mainDeck;
    Deck * onTable;
    Deck ** hands;
    uint8_t numHands;
} Table;



//------------- FUNCTIONS ------------- 

extern __declspec(dllexport) void construct_table(uint8_t numHands);
extern __declspec(dllexport) void destroy_table();
extern __declspec(dllexport) void reset_table();

extern __declspec(dllexport) void shuffle_main();
extern __declspec(dllexport) bool draw_main_to_table();
extern __declspec(dllexport) bool draw_main_to_hand(uint8_t index);
extern __declspec(dllexport) bool draw_hand_to_table(uint8_t hand_index, uint8_t card_index);
extern __declspec(dllexport) bool draw_table_to_hand(uint8_t hand_index, uint8_t card_index);

void put_deck_json(char * buff, Deck * deck);
extern __declspec(dllexport) void put_table_json(char * buff);

#endif //table.h
