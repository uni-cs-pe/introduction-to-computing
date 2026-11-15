// Intercambiar dos variables necesita una tercera.
#include <stdio.h>

int main(void) {
    int left = 4;
    int right = 9;

    int saved = left;           // guardamos left antes de perderlo
    left = right;
    right = saved;

    printf("left = %d, right = %d\n", left, right);
    return 0;
}
