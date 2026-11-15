#include <stdio.h>

// ERROR: los dos ciclos usan la misma variable i.
int main(void) {
    int i;

    for (i = 1; i <= 3; i++) {
        for (i = 1; i <= 3; i++) {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
