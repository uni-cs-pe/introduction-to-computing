// Comparar double con == falla; se compara con una tolerancia.
#include <math.h>
#include <stdio.h>

int main(void) {
    double sum = 0.1 + 0.2;
    double target = 0.3;
    double tolerance = 0.000000001;

    printf("sum == target vale %d\n", sum == target);
    printf("fabs(sum - target) < tolerance vale %d\n", fabs(sum - target) < tolerance);
    return 0;
}
