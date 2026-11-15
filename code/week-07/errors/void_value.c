#include <stdio.h>

void print_twice(int x) {
    printf("%d\n", x * 2);
}

// Error: una función void no devuelve un valor que se pueda guardar.
int main(void) {
    int y = print_twice(4);
    printf("%d\n", y);
    return 0;
}
