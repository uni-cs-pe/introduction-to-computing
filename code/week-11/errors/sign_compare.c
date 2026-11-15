// Advertencia: comparar un int con el resultado de strlen mezcla signo y sin signo.
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "sol";

    for (int i = 0; i < strlen(s); i++) {
        printf("%c\n", s[i]);
    }
    return 0;
}
