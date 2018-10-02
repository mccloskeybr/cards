CC=gcc
CFLAGS=-Wall -g -fPIC
DEPS=cards.h log.h table.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: main.o cards.o log.o table.o
	$(CC) -o main main.o cards.o log.o table.o

library: cards.o log.o table.o
	$(CC) -shared -o cards_backend.so cards.o log.o table.o

clean:
	rm -f main main.o cards.o log.o table.o cards_backend.so
