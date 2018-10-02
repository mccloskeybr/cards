#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "cards.h"
#include "log.h"
#include "table.h"

const char main_classname[] = "main.c";

extern Table * TABLE;

/**
 * Contains the main program loop
 * Commands are parsed and dealt with here
 */
int main() {

    construct_table(4);

    char cmd[100];
    bool quit = false;
    while (!quit) {

        printf("\n >: ");
        scanf("%s", cmd);

        if (strcmp(cmd, "help") == 0) {
            printf( \
                "the following commands are supported:\n \
                 quit\n \
                 reset_table\n \
                 shuffle\n \
                 print_main\n \
                 print_hand <index>\n \
                 draw_main_to_table\n \
                 draw_main_to_hand <index>\n \
                 draw_hand_to_table <hand_index> <card_index>\n \
                 draw_table_to_hand <hand_index> <card_index>\n \
                 draw_hand_to_discard <hand_index> <card_index>\n \
                 draw_table_to_discard <index>\n");
        }

        else if (strcmp(cmd, "quit") == 0) {
            quit = true;
            printf("exiting the program.\n");
        }

        else if (strcmp(cmd, "reset_table") == 0) {
            reset_table();
            printf("reset the table.\n");
        }

        else if (strcmp(cmd, "shuffle") == 0) {
            shuffle_main();
            printf("shuffled the main deck.\n");
        }

        else if (strcmp(cmd, "print_main") == 0) {
            print_deck(TABLE->mainDeck);
        }

        else if (strcmp(cmd, "print_hand") == 0) {

            int index = -1;
            scanf("%d", &index);

            if (index >= 0 && index < TABLE->numHands) {
                print_deck(TABLE->hands[index]);
            }
            else {
                printf("Invalid index.\n");
            }


        }

        else if (strcmp(cmd, "print_table") == 0) {

            print_deck(TABLE->onTable);

        }

        else if (strcmp(cmd, "draw_main_to_table") == 0) {

            draw_main_to_table();
            print_deck(TABLE->onTable);

        }

        else if (strcmp(cmd, "draw_main_to_hand") == 0) {

            int index = -1;
            scanf("%d", &index);

            if(index >= 0 && index < TABLE->numHands) {
                
                draw_main_to_hand(index);
                print_deck(TABLE->hands[index]);

            }
            else {
                printf("Invalid index.\n");
            }

        }

        else if (strcmp(cmd, "draw_hand_to_table") == 0) {

            int hand_index = -1;
            int card_index = -1;

            scanf("%d %d", &hand_index, &card_index);
            if (hand_index >= 0 && hand_index < TABLE->numHands && \
                card_index >= 0 && card_index <= TABLE->hands[hand_index]->currCard) {

                draw_hand_to_table(hand_index, card_index);
                print_deck(TABLE->onTable);

            }
            else {
                printf("Invalid index(indicies).\n");
            }


        }


        else if (strcmp(cmd, "draw_table_to_hand") == 0) {

            int hand_index = -1;
            int card_index = -1;

            scanf("%d %d", &hand_index, &card_index);
            if (hand_index >= 0 && hand_index < TABLE->numHands && \
                card_index >= 0 && card_index <= TABLE->onTable->currCard) {

                draw_table_to_hand(hand_index, card_index);
                print_deck(TABLE->hands[hand_index]);

            }
            else {
                printf("Invalid index(indicies).\n");
            }


        }

        else if (strcmp(cmd, "draw_table_to_discard") == 0) {

            int index = -1;

            scanf("%d", &index);
            if (index >= 0 && index <= TABLE->onTable->currCard) {

                draw_table_to_discard(index);
                print_deck(TABLE->discard);

            }
            else {
                printf("Invalid index(indicies).\n");
            }


        }

        else if (strcmp(cmd, "draw_hand_to_discard") == 0) {

            int hand_index = -1;
            int card_index = -1;

            scanf("%d %d", &hand_index, &card_index);
            if (hand_index >= 0 && hand_index < TABLE->numHands && \
                card_index >= 0 && card_index <= TABLE->hands[hand_index]->currCard) {

                draw_hand_to_discard(hand_index, card_index);
                print_deck(TABLE->discard);

            }
            else {
                printf("Invalid index(indicies).\n");
            }


        }


        else {
            printf("'%s': command not recognized.\n", cmd);
        }

        char * buff = calloc(1000, sizeof(char));
        put_table_json(buff);
        free(buff);

    }

    destroy_table(TABLE);

    return 0;

}
