// El tamaño de un struct puede ser mayor que la suma de sus campos.
#include <stdio.h>

struct mixed {
    char first;
    int number;
    char last;
};

struct sorted {
    int number;
    char first;
    char last;
};

int main(void) {
    printf("sizeof(char) = %zu, sizeof(int) = %zu\n", sizeof(char), sizeof(int));
    printf("sizeof(struct mixed) = %zu\n", sizeof(struct mixed));
    printf("sizeof(struct sorted) = %zu\n", sizeof(struct sorted));
    return 0;
}
