// Error: con la cadena vacía, s[strlen(s) - 1] está fuera del arreglo.
#include <stdio.h>
#include <string.h>

char last_char(const char s[]) {
    return s[strlen(s) - 1];
}

int main(void) {
    char word[] = "sol";
    char empty[] = "";

    printf("%c\n", last_char(word));
    printf("%c\n", last_char(empty));
    return 0;
}
