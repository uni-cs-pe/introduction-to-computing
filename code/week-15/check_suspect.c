// Parte de make test-lab: llama a una función de suspect.c con los datos que recibe
// e imprime el resultado. Las respuestas esperadas están en test_lab.py.
//   prime N          is_prime(N)
//   max A B C ...    max_of_array con esos números
//   copy SIZE TEXT   copy_text en un destino de exactamente SIZE bytes
#include <stdio.h>
#include <stdlib.h>

#define MAX_ITEMS 16

int is_prime(int n);
int max_of_array(const int a[], int n);
void copy_text(char dest[], const char src[], int size);

int main(int argc, char *argv[]) {
    if (argc < 3) {
        return 2;
    }
    if (argv[1][0] == 'p') {
        printf("%d\n", is_prime(atoi(argv[2])));
    } else if (argv[1][0] == 'm') {
        int a[MAX_ITEMS];
        int n = argc - 2;
        if (n > MAX_ITEMS) {
            return 2;
        }
        for (int i = 0; i < n; i++) {
            a[i] = atoi(argv[i + 2]);
        }
        printf("%d\n", max_of_array(a, n));
    } else {
        // Solo se usan estos tamaños, cada uno con su arreglo exacto. Los bytes de partida
        // no son '\0', para que se note si la función no termina la cadena.
        int size = atoi(argv[2]);
        const char *text = argc > 3 ? argv[3] : "";
        char one[1] = {'X'};
        char two[2] = {'X', 'X'};
        char three[3] = {'X', 'X', 'X'};
        char five[5] = {'X', 'X', 'X', 'X', 'X'};
        if (size == 1) {
            copy_text(one, text, 1);
            printf("[%s]\n", one);
        } else if (size == 2) {
            copy_text(two, text, 2);
            printf("[%s]\n", two);
        } else if (size == 3) {
            copy_text(three, text, 3);
            printf("[%s]\n", three);
        } else if (size == 5) {
            copy_text(five, text, 5);
            printf("[%s]\n", five);
        } else {
            return 2;
        }
    }
    return 0;
}
