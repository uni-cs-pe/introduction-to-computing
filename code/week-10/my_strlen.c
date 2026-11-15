// La longitud de una cadena: los bytes que hay antes del '\0'.
#include <assert.h>
#include <stdio.h>

int my_strlen(const char s[]) {
    int i = 0;
    while (s[i] != '\0') {
        i++;
    }
    return i;
}

int main(void) {
    assert(my_strlen("") == 0);
    assert(my_strlen("a") == 1);
    assert(my_strlen("hola") == 4);

    char t[8] = "hola";
    printf("my_strlen(t) = %d\n", my_strlen(t));
    printf("sizeof(t) = %zu\n", sizeof(t));
    printf("my_strlen(\"ano\") = %d\n", my_strlen("ano"));
    printf("my_strlen(\"año\") = %d\n", my_strlen("año"));
    return 0;
}
