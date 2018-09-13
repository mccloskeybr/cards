
#include <stdlib.h>
#include <stdio.h>

#define LOGNAME "LOG.txt"

struct Log {
    FILE * file;
};

struct Log * construct_log(char * name);
void destroy_log(struct Log * log);

void write_to_log(const char * classname, char * buff);

