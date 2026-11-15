// strchr y strstr devuelven una dirección, o NULL si no encuentran nada.
#include <stdio.h>
#include <string.h>

int main(void) {
    char email[] = "ana@example.com";
    char text[] = "el año pasado llovió en Lima";

    if (strchr(email, '@') != NULL) {
        printf("Tiene @: %s\n", strchr(email, '@'));
    }
    if (strchr(email, '#') == NULL) {
        printf("No tiene #\n");
    }
    if (strstr(text, "Lima") != NULL) {
        printf("Desde Lima: %s\n", strstr(text, "Lima"));
    }
    if (strstr(text, "lima") == NULL) {
        printf("lima, en minúsculas, no aparece\n");
    }
    if (strstr(text, "ñ") != NULL) {
        printf("Desde la ñ: %s\n", strstr(text, "ñ"));
    }
    // &text[3] es la dirección del byte 3: lo que recibe la función empieza ahí.
    printf("Desde el byte 3: %s\n", &text[3]);
    if (strstr(text, "el") != NULL) {
        printf("Desde el byte 0 hay un el\n");
    }
    if (strstr(&text[1], "el") == NULL) {
        printf("Desde el byte 1 no hay ninguno\n");
    }
    return 0;
}
