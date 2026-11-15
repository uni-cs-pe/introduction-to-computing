#include <stdio.h>

// Error: main usa cube antes de que el compilador la conozca.
int main(void) {
    printf("%d\n", cube(3));
    return 0;
}

int cube(int x) {
    return x * x * x;
}
