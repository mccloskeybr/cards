#include "cards.h"
#include "log.h"
#include "table.h"

const char main_classname[] = "main.c";

struct Table * TABLE;

void init(uint8_t numHands) {

    TABLE = construct_table(numHands);

    write_to_log(main_classname, "Successfully initialized.");

}


int main() {

    init(1);
    shuffle(TABLE->mainDeck);
    print_deck(TABLE->mainDeck);

    draw_main_to_table(TABLE);

    print_deck(TABLE->mainDeck);
    print_deck(TABLE->onTable);

    reset_table(TABLE);

    print_deck(TABLE->mainDeck);

    destroy_table(TABLE);

    return 0;

}
