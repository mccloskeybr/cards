CC=gcc
CFLAGS=-Wall -g
DEPS=cards.h log.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: main.o cards.o log.o
	$(CC) -o main main.o cards.o log.o

clean:
	rm -f main main.o cards.o log.o
