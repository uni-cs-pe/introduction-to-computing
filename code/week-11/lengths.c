// strlen cuenta bytes hasta el '\0'. Devuelve size_t, un tipo sin signo.
#include <stdio.h>
#include <string.h>

int main(void) {
    char t[8] = "hola";

    printf("strlen(t) = %zu\n", strlen(t));
    printf("sizeof(t) = %zu\n", sizeof(t));
    printf("strlen(\"\") = %zu\n", strlen(""));
    printf("strlen(\"año\") = %zu\n", strlen("año"));

    // Para recorrer con un int, se guarda la longitud una vez, con un cast.
    int n = (int) strlen(t);
    for (int i = n - 1; i >= 0; i--) {
        printf("%c", t[i]);
    }
    printf("\n");
    return 0;
}
