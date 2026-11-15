// Error a propósito: restar para comparar parece cómodo, pero la resta puede no caber.
#include <stdio.h>
#include <stdlib.h>

#define N 3

int compare_subtract(const void *first, const void *second) {
    int x = *(const int *) first;
    int y = *(const int *) second;
    return x - y;
}

int main(void) {
    int a[N] = {2000000000, -2000000000, 5};

    qsort(a, N, sizeof(a[0]), compare_subtract);

    for (int i = 0; i < N; i++) {
        printf(" %d", a[i]);
    }
    printf("\n");
    return 0;
}
