#include <stdio.h>

// Recorre los 36 resultados de dos dados, una vez por cada suma de 2 a 12.
int main(void) {
    for (int target = 2; target <= 12; target++) {
        int ways = 0;

        for (int d1 = 1; d1 <= 6; d1++) {
            for (int d2 = 1; d2 <= 6; d2++) {
                if (d1 + d2 == target) {
                    ways++;
                }
            }
        }
        printf("Suma %2d: %d de 36, %.4f\n", target, ways, (double) ways / 36);
    }
    return 0;
}
