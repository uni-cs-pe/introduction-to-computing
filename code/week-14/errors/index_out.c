// Lee un índice y lo usa sin revisarlo. Con un índice fuera de rango, el comportamiento es indefinido.
#include <stdio.h>

int main(void) {
    int values[5] = {14, 9, 17, 11, 20};
    int index;
    if (scanf("%d", &index) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("%d\n", values[index]);
    return 0;
}
