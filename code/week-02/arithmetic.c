// Precedencia: primero * / %, después + -. A igual nivel, de izquierda a derecha.
#include <stdio.h>

int main(void) {
    printf("10 - 2 * 3 = %d\n", 10 - 2 * 3);
    printf("(10 - 2) * 3 = %d\n", (10 - 2) * 3);
    printf("20 / 2 * 5 = %d\n", 20 / 2 * 5);
    printf("10 - 4 - 3 = %d\n", 10 - 4 - 3);
    printf("7 + 8 %% 3 * 2 = %d\n", 7 + 8 % 3 * 2);
    return 0;
}
