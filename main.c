#include "cards.h"
#include "log.h"
#include "table.h"

const char main_classname[] = "main.c";

struct Table * TABLE;

void init(uint8_t numHands) {

    TABLE = construct_table(numHands);

    write_to_log(main_classname, "initialized MAINDECK TABLE HANDS");

}


int main() {

    init(1);

    print_deck(TABLE->mainDeck);

    destroy_table(TABLE);


    return 0;

}
