#ifndef __LOG_H
#define __LOG_H

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define LOGNAME "LOG.txt"

struct Log {
    FILE * file;
};

struct Log * construct_log(char * name);
void destroy_log(struct Log * log);

void write_to_log(const char * classname, char * buff);

#endif //log.h
