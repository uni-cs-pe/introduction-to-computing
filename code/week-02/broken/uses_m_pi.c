// Error a propósito: con -std=c17, math.h no define M_PI.
#include <math.h>
#include <stdio.h>

int main(void) {
    printf("%f\n", M_PI);
    return 0;
}
