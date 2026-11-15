// Error: si el texto no cabe, strncpy no pone '\0', y %s sigue de largo.
#include <stdio.h>
#include <string.h>

#define SIZE 5

void fill(char dest[], const char src[]) {
    strncpy(dest, src, SIZE);
}

int main(void) {
    char word[SIZE];

    fill(word, "estrella");
    printf("%s\n", word);
    return 0;
}
