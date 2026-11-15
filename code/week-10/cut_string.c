// %s se detiene en el primer '\0', aunque el arreglo siga.
#include <stdio.h>

int main(void) {
    char s[] = "hola";

    printf("%s\n", s);
    s[0] = 'H';
    printf("%s\n", s);
    s[2] = '\0';
    printf("%s\n", s);
    printf("sizeof(s) sigue siendo %zu\n", sizeof(s));
    return 0;
}
