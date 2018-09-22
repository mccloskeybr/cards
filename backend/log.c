#include "log.h"

static struct Log * log = 0;


/** ---------------- CON/DESTRUCTORS ---------------- **/ 


/**
 * Constructs a log struct
 */
struct Log * construct_log(char * name) {
    
    struct Log * log = malloc(sizeof(struct Log));
    
    log->file = fopen(name, "w");
    log->name = name;
    
    return log;

}

/**
 * Destroys a log struct
 */
void destroy_log(struct Log * log) {

    if (log != 0) {
        fclose(log->file);
        free(log);
    }

}


/** ---------------- OUTPUT ---------------- **/ 


/**
 * Writes to the log in the following format:
 *  [classname] : buff
 * where classname and buff (message) are passed in
 */
void write_to_log(const char * classname, char * buff) {

    if (log == 0) {
        log = construct_log("LOG.txt");
    }

    time_t timer;
    time(&timer);
    struct tm * tm_info = localtime(&timer);

    char * time_buff = calloc(26, sizeof(char));
    strftime(time_buff, 26, "%Y-%m-%d %H:%M:%S", tm_info);

    fprintf(log->file, "%s [%-15.15s] : %s\n", time_buff, classname, buff);

    free(time_buff);

}
