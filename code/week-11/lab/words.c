// Laboratorio, parte 1: contar cuántas veces aparece una palabra en un texto.
//
// Escriban count_word usando strstr. Borren las líneas (void): solo están para que el
// archivo compile sin advertencias mientras tanto.
//
// En main hay algunas pruebas. Agreguen más con assert: casos normales y bordes.
//
// Pruébenlo con make test-lab.
#include <assert.h>
#include <stdio.h>
#include <string.h>

// Devuelve cuántas veces aparece word dentro de text, según estas reglas:
//   - Se compara byte por byte: 'S' y 's' son distintos.
//   - No hace falta que sea una palabra completa: "sol" aparece una vez en "girasol".
//   - Las apariciones no se pisan: al encontrar una, se sigue buscando después de ella.
//     "ana" aparece una vez en "banana", y "aa" aparece 2 veces en "aaaaa".
//   - Si word es la cadena vacía, devuelve 0.
// Basta buscar desde &text[i], como explican los apuntes: no hace falta declarar punteros.
int count_word(const char text[], const char word[]) {
    (void) text;
    (void) word;
    return 0;
}

int main(void) {
    assert(count_word("sol y luna", "sol") == 1);
    assert(count_word("sol y sol", "sol") == 2);
    assert(count_word("sol y luna", "mar") == 0);
    printf("Todas las pruebas pasaron\n");
    return 0;
}
