// Código de la transcripción A de lab/transcripts.md. Es un ejemplo escrito para la actividad.
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
    printf("Pruebas pasadas\n");
    return 0;
}
