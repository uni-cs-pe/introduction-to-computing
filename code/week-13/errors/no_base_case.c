// Error a propósito: una función recursiva sin caso base.
#include <stdio.h>

long long sum_down(int n) {
    return n + sum_down(n - 1);
}

int main(void) {
    printf("%lld\n", sum_down(3));
    return 0;
}
