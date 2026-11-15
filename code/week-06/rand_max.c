#include <stdio.h>
#include <stdlib.h>

// Escribe RAND_MAX y los primeros números de rand, sin llamar a srand.
int main(void) {
    printf("RAND_MAX = %d\n", RAND_MAX);

    for (int i = 1; i <= 5; i++) {
        printf("%d\n", rand());
    }
    return 0;
}
