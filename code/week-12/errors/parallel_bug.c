// Arreglos paralelos: se elimina en uno y se olvida el otro. Compila sin advertencias.
#include <stdio.h>

#define NAME_SIZE 20
#define N 3

int main(void) {
    char names[N][NAME_SIZE] = {"Ana", "Bruno", "Carla"};
    int grades[N] = {14, 9, 11};
    int n = N;

    // Bruno se retira: se mueven las notas, y se olvidan los nombres.
    for (int i = 1; i < n - 1; i++) {
        grades[i] = grades[i + 1];
    }
    n = n - 1;

    for (int i = 0; i < n; i++) {
        printf("%s: %d\n", names[i], grades[i]);
    }
    return 0;
}
