// Laboratorio, parte 1: sus pruebas de las funciones de lab/suspect.c.
//
// Cada función de abajo trae una prueba, y las tres pasan aunque suspect.c tiene bugs.
// Agreguen asserts hasta que cada grupo encuentre el bug de su función. Piensen en los
// bordes. Para copy_text, usen un destino exactamente del tamaño que le pasan: el
// sanitizer solo puede avisar si la escritura se sale de ese arreglo.
//
// Compilen y corran con:
//     make build/lab/tests && build/lab/tests
#include <assert.h>
#include <stdio.h>
#include <string.h>

int is_prime(int n);
int max_of_array(const int a[], int n);
void copy_text(char dest[], const char src[], int size);

void check_is_prime(void) {
    assert(is_prime(7) == 1);
    assert(is_prime(8) == 0);
}

void check_max_of_array(void) {
    int grades[3] = {14, 9, 17};
    assert(max_of_array(grades, 3) == 17);
}

void check_copy_text(void) {
    char word[20];
    copy_text(word, "hola", 20);
    assert(strcmp(word, "hola") == 0);
}

int main(void) {
    check_is_prime();
    check_max_of_array();
    check_copy_text();
    printf("Todas las pruebas pasaron\n");
    return 0;
}
