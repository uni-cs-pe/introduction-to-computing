// Si el compilador ve el texto, avisa que strncpy lo va a cortar.
#include <stdio.h>
#include <string.h>

int main(void) {
    char word[5];

    strncpy(word, "estrella", 5);
    printf("%c\n", word[0]);
    return 0;
}
