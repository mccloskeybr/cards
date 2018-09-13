#include "log.h"

struct Log * log = 0;


/** ---------------- CON/DESTRUCTORS ---------------- **/ 


/**
 * Constructs a log struct
 */
struct Log * construct_log(char * name) {
    
    struct Log * log = malloc(sizeof(struct Log));
    
    log->file = fopen(name, "w");
    
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
        log = construct_log(LOGNAME);
    }

    fprintf(log->file, "[%-15.15s] : %s\n", classname, buff);

}
