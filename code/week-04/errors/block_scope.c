#include <stdio.h>

// Error a propósito: una variable declarada entre llaves solo existe ahí dentro.
int main(void) {
    int n = 4;

    if (n > 0) {
        int twice = n * 2;
        printf("%d\n", twice);
    }
    printf("%d\n", twice);

    return 0;
}
