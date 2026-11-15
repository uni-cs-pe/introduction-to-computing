// Vuelto con la menor cantidad de monedas, usando / y % en lugar de un ciclo.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    int remaining = 0;

    printf("Vuelto en céntimos: ");
    scanf("%d", &remaining);

    int coins_500 = remaining / 500;
    remaining = remaining % 500;
    int coins_200 = remaining / 200;
    remaining = remaining % 200;
    int coins_100 = remaining / 100;
    remaining = remaining % 100;
    int coins_50 = remaining / 50;
    remaining = remaining % 50;
    int coins_20 = remaining / 20;
    remaining = remaining % 20;
    int coins_10 = remaining / 10;
    remaining = remaining % 10;

    printf("5 soles: %d\n", coins_500);
    printf("2 soles: %d\n", coins_200);
    printf("1 sol: %d\n", coins_100);
    printf("50 céntimos: %d\n", coins_50);
    printf("20 céntimos: %d\n", coins_20);
    printf("10 céntimos: %d\n", coins_10);
    printf("Sin cubrir: %d céntimos\n", remaining);
    return 0;
}
