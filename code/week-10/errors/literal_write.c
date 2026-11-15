// A propósito: intenta cambiar un literal de cadena. Es comportamiento indefinido.
#include <stdio.h>

void set_first(char s[], char c) {
    s[0] = c;
}

int main(void) {
    char copy[] = "hola";

    set_first(copy, 'H');
    printf("%s\n", copy);
    set_first("hola", 'H');
    printf("no llegamos aquí, o no deberíamos\n");
    return 0;
}
