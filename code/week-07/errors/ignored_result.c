#include <stdio.h>

int square(int x) {
    return x * x;
}

// El resultado de square no se guarda: se pierde. gcc no avisa.
int main(void) {
    int a = 5;
    square(a);
    printf("%d\n", a);
    return 0;
}
