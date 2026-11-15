#include <stdio.h>

// Las tablas de verdad de &&, || y !, calculadas por el propio C.
int main(void) {
    printf("a b | a&&b a||b !a\n");
    printf("0 0 | %4d %4d %2d\n", 0 && 0, 0 || 0, !0);
    printf("0 1 | %4d %4d %2d\n", 0 && 1, 0 || 1, !0);
    printf("1 0 | %4d %4d %2d\n", 1 && 0, 1 || 0, !1);
    printf("1 1 | %4d %4d %2d\n", 1 && 1, 1 || 1, !1);

    return 0;
}
