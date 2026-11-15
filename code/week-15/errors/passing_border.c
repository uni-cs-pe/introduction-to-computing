// La función de la transcripción A, con la prueba que encuentra su bug: una nota de 11.
#include <assert.h>
#include <stdio.h>

// Cuenta cuántas notas están aprobadas. Se aprueba con 11 o más.
int count_passing(const int grades[], int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (grades[i] > 11) {
            count++;
        }
    }
    return count;
}

int main(void) {
    int grades[5] = {14, 9, 17, 8, 20};
    assert(count_passing(grades, 5) == 3);

    int border[3] = {11, 10, 12};
    assert(count_passing(border, 3) == 2);
    printf("Las dos pruebas pasaron\n");
    return 0;
}
