#include <stdio.h>

// La aritmética va antes que las comparaciones, y estas antes que && y ||.
int main(void) {
    int x = 5;
    int y = 2;

    printf("%d\n", x + 1 > y * 3);
    printf("%d\n", x > 3 && x < 10);
    printf("%d\n", (x > 3 && y > 3) || y == 2);
    printf("%d\n", x > 3 && (y > 3 || y == 2));
    printf("%d\n", !(x > 3));

    return 0;
}
