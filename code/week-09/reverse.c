#include <stdio.h>

#define MAX_VALUES 100

// Lee n enteros y los escribe en orden inverso.
int main(void) {
    int values[MAX_VALUES];
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    if (n < 1 || n > MAX_VALUES) {
        printf("n debe estar entre 1 y %d\n", MAX_VALUES);
        return 1;
    }

    for (int i = 0; i < n; i++) {
        if (scanf("%d", &values[i]) != 1) {
            printf("Entrada inválida\n");
            return 1;
        }
    }

    for (int i = n - 1; i >= 0; i--) {
        printf("%d\n", values[i]);
    }
    return 0;
}
