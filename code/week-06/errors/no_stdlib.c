#include <stdio.h>

// ERROR: rand se declara en stdlib.h, y falta incluirlo.
int main(void) {
    printf("%d\n", rand());
    return 0;
}
