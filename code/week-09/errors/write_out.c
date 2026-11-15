#include <stdio.h>

#define SIZE 4

// Bug: no revisa el índice que lee. Se usa para ver qué pasa al salirse.
int main(void) {
    int before = 111;
    int values[SIZE] = {1, 2, 3, 4};
    int after = 222;
    int index;

    if (scanf("%d", &index) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    values[index] = 99;

    printf("values[%d] = %d\n", index, values[index]);
    printf("before = %d, after = %d\n", before, after);
    return 0;
}
