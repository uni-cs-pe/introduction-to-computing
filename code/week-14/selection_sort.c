// Ordena con selección, como en la semana 13. Crece como N al cuadrado.
#include <stdio.h>

#define MAX 100000

int main(void) {
    int values[MAX];
    int n;
    if (scanf("%d", &n) != 1 || n < 1 || n > MAX) {
        printf("Se espera un número entre 1 y %d\n", MAX);
        return 1;
    }
    for (int i = 0; i < n; i++) {
        values[i] = (i * 7919) % 100003;
    }
    for (int i = 0; i < n - 1; i++) {
        int smallest = i;
        for (int j = i + 1; j < n; j++) {
            if (values[j] < values[smallest]) {
                smallest = j;
            }
        }
        int saved = values[i];
        values[i] = values[smallest];
        values[smallest] = saved;
    }
    printf("menor: %d, mayor: %d\n", values[0], values[n - 1]);
    return 0;
}
