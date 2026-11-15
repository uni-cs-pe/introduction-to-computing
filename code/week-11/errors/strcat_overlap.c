// Error: el origen y el destino de strcat no pueden pisarse.
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[20] = "hola";

    strcat(s, s);
    printf("%s\n", s);
    return 0;
}
