#include <stdio.h>

int twice(int x) {
    int result = x * 2;
    return result;
}

int triple(int x) {
    int result = x * 3;
    return result;
}

int main(void) {
    int result = twice(5) + triple(5);
    printf("%d\n", result);
    return 0;
}
