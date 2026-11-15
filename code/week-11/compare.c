// strcmp: solo importa el signo de lo que devuelve.
#include <stdio.h>
#include <string.h>

void show_order(const char a[], const char b[]) {
    int result = strcmp(a, b);
    if (result < 0) {
        printf("\"%s\" va antes que \"%s\"\n", a, b);
    } else if (result > 0) {
        printf("\"%s\" va después de \"%s\"\n", a, b);
    } else {
        printf("\"%s\" y \"%s\" son iguales\n", a, b);
    }
}

int main(void) {
    show_order("ana", "ana");
    show_order("ana", "ano");
    show_order("an", "ana");
    show_order("sol", "luna");
    show_order("Z", "a");
    show_order("z", "ñ");
    return 0;
}
