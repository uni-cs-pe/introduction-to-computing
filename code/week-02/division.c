// Entre dos enteros, / da un entero. Si uno es double, da un double.
#include <stdio.h>

int main(void) {
    printf("17 / 5 = %d\n", 17 / 5);
    printf("17 %% 5 = %d\n", 17 % 5);
    printf("17.0 / 5 = %f\n", 17.0 / 5);
    printf("17 / 5.0 = %f\n", 17 / 5.0);
    printf("-17 / 5 = %d\n", -17 / 5);
    printf("-17 %% 5 = %d\n", -17 % 5);
    printf("17 %% -5 = %d\n", 17 % -5);
    return 0;
}
