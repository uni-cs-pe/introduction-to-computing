// A propósito: abre el espacio moviendo desde el inicio y pisa los valores.
#include <stdio.h>

int main(void) {
    int v[5] = {10, 20, 30};
    int n = 3;
    int pos = 1;

    for (int i = pos; i < n; i++) {
        v[i + 1] = v[i];
    }
    v[pos] = 99;
    n = n + 1;

    for (int i = 0; i < n; i++) {
        printf(" %d", v[i]);
    }
    printf("\n");
    return 0;
}
