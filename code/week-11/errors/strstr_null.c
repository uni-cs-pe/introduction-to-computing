// Error: usar lo que devuelve strstr sin revisar si es NULL.
#include <stdio.h>
#include <string.h>

int main(void) {
    char text[] = "sol y luna";

    printf("%s\n", strstr(text, "luna"));
    printf("%s\n", strstr(text, "mar"));
    return 0;
}
