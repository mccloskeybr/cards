#include "cards.h"
#include "log.h"

const char classname[] = "main.c";

struct Deck * MAINDECK;
struct Deck * TABLE;
struct Deck ** HANDS;

void init(uint8_t numHands) {

    MAINDECK = construct_std_deck();
    TABLE = construct_deck(MAINDECK->maxCards);
    HANDS = malloc(numHands * sizeof(struct Deck *));
 
    uint8_t i;
    for (i = 0; i < numHands; i++) {
        HANDS[i] = construct_deck(MAINDECK->maxCards);
    }

    write_to_log(classname, "initialized MAINDECK TABLE HANDS");

}


int main() {

    init(1);

    print_deck(MAINDECK);

    destroy_deck(MAINDECK);

    return 0;

}
