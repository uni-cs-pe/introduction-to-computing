#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// ERROR: siembra de nuevo en cada vuelta, con la misma hora.
int main(void) {
    for (int i = 1; i <= 10; i++) {
        srand((unsigned) time(NULL));
        printf("%d ", 1 + rand() % 6);
    }
    printf("\n");
    return 0;
}
