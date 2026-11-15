#include <stdio.h>

// Compila, con una advertencia, pero no compara los elementos.
int main(void) {
    int first[3] = {1, 2, 3};
    int second[3] = {1, 2, 3};

    if (first == second) {
        printf("iguales\n");
    } else {
        printf("distintos\n");
    }
    return 0;
}
