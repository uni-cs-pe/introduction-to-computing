// Lo que devuelve sscanf con distintas líneas.
#include <stdio.h>

#define NAME_SIZE 20
#define N_LINES 8

void try_line(const char line[]) {
    char name[NAME_SIZE];
    int a;
    int b;
    int c;
    char extra[2];
    int fields = sscanf(line, "%19s %d %d %d %1s", name, &a, &b, &c, extra);
    printf("%2d  \"%s\"\n", fields, line);
}

int main(void) {
    const char lines[N_LINES][64] = {
        "Ana 14 9 17",
        "  Ana   14 9   17  ",
        "Ana 14 9",
        "Ana diez 9 17",
        "Ana 14.5 9 17",
        "Ana 14 9 17 5",
        "Maria_de_los_Angeles_Quispe 14 9 17",
        "",
    };
    for (int i = 0; i < N_LINES; i++) {
        try_line(lines[i]);
    }
    return 0;
}
