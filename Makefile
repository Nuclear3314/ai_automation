CC = gcc
CFLAGS = -Wall -Wextra -std=c11
TARGET = main
OBJECTS = main.o hello.o

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJECTS)

clean-win:
	rm -f $(TARGET).exe $(OBJECTS)