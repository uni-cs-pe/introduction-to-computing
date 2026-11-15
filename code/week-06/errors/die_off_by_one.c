#include <stdio.h>
#include <stdlib.h>

// ERROR: rand() % 6 da de 0 a 5, no de 1 a 6.
int main(void) {
    int smallest = 100;
    int largest = -100;

    srand(42);

    for (int i = 1; i <= 100000; i++) {
        int die = rand() % 6;

        if (die < smallest) {
            smallest = die;
        }
        if (die > largest) {
            largest = die;
        }
    }

    printf("Menor: %d\n", smallest);
    printf("Mayor: %d\n", largest);
    return 0;
}
