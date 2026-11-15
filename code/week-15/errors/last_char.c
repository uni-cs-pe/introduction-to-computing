// Pasa la prueba con "hola", y falla con la cadena vacía: lee s[-1], fuera del arreglo.
#include <stdio.h>
#include <string.h>

char last_char(const char s[]) {
    int n = strlen(s);
    return s[n - 1];
}

int main(void) {
    char word[] = "hola";
    char empty[] = "";
    printf("%c\n", last_char(word));
    fflush(stdout);    // para que se vea antes del informe del sanitizer
    printf("%c\n", last_char(empty));
    return 0;
}
