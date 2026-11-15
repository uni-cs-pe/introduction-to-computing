#include <stdio.h>

// Una suma simple, para mirar su ensamblador con gcc -S.
int main(void) {
    int a = 2;
    int b = 3;
    int c = a + b;

    printf("%d\n", c);
    return 0;
}
