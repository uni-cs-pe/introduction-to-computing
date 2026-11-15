// Código de la transcripción B de lab/transcripts.md. Es un ejemplo escrito para la actividad.
#include <assert.h>
#include <stdio.h>

// Cuenta cuántas veces aparece el byte c en la cadena s.
int count_char(const char s[], char c) {
    int count = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == c) {
            count++;
        }
    }
    return count;
}

int main(void) {
    assert(count_char("banana", 'a') == 3);
    printf("Pruebas pasadas\n");
    return 0;
}
