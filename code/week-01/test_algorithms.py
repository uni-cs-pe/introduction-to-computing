"""Comprueba los algoritmos que el capítulo sigue a mano. Cada función copia, paso
a paso, un pseudocódigo de los apuntes: give_change es dar_vuelto, five_sol_coins es
monedas_de_cinco y larger_of_two es mayor_de_dos."""
import unittest

COINS = (500, 200, 100, 50, 20, 10)


def give_change(amount):
    """Devuelve las monedas, cada valor restante y lo que queda al final."""
    coins, remaining = [], []
    for coin in COINS:
        while amount >= coin:
            amount -= coin
            coins.append(coin)
            remaining.append(amount)
    return coins, remaining, amount


def five_sol_coins(amount):
    count = 0
    while amount >= 500:
        amount -= 500
        count += 1
    return count, amount


def larger_of_two(a, b):
    if a > b:
        return a
    return b


def greedy_count(amount, coins):
    count = 0
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            count += 1
    return count


def fewest_count(amount, coins):
    """Menor cantidad de monedas, probando todas las combinaciones posibles."""
    best = [0] + [None] * amount
    for value in range(1, amount + 1):
        options = [best[value - c] for c in coins
                   if c <= value and best[value - c] is not None]
        best[value] = min(options) + 1 if options else None
    return best[amount]


def final_grade(ep, ef, practicas):
    pp = sum(sorted(practicas, reverse=True)[:3]) / 3
    return pp, (ep + 2 * ef + pp) / 4


class ChangeTest(unittest.TestCase):
    def test_780_table(self):
        coins, remaining, left = give_change(780)
        self.assertEqual(coins, [500, 200, 50, 20, 10])
        self.assertEqual(remaining, [280, 80, 30, 10, 0])
        self.assertEqual(left, 0)

    def test_1360(self):
        coins, _, left = give_change(1360)
        self.assertEqual(coins, [500, 500, 200, 100, 50, 10])
        self.assertEqual(left, 0)

    def test_785_leaves_five(self):
        coins, _, left = give_change(785)
        self.assertEqual(coins, [500, 200, 50, 20, 10])
        self.assertEqual(left, 5)

    def test_zero_gives_no_coins(self):
        self.assertEqual(give_change(0), ([], [], 0))

    def test_greedy_is_fewest_for_these_coins(self):
        # Todos los montos hasta S/ 100, de 10 en 10 céntimos.
        for amount in range(0, 10001, 10):
            self.assertEqual(greedy_count(amount, COINS),
                             fewest_count(amount, COINS), amount)

    def test_greedy_is_not_always_fewest(self):
        self.assertEqual(greedy_count(6, (1, 3, 4)), 3)
        self.assertEqual(fewest_count(6, (1, 3, 4)), 2)
        # Ejercicio 7 de los apuntes.
        self.assertEqual(greedy_count(10, (1, 5, 7)), 4)
        self.assertEqual(fewest_count(10, (1, 5, 7)), 2)


class SmallAlgorithmsTest(unittest.TestCase):
    def test_five_sol_coins(self):
        self.assertEqual(five_sol_coins(1300), (2, 300))
        self.assertEqual(five_sol_coins(780), (1, 280))
        self.assertEqual(five_sol_coins(300), (0, 300))

    def test_larger_of_two(self):
        self.assertEqual(larger_of_two(14, 17), 17)
        self.assertEqual(larger_of_two(17, 14), 17)
        self.assertEqual(larger_of_two(9, 9), 9)

    def test_grade_example(self):
        pp, final = final_grade(12, 14, (11, 15, 13, 9))
        self.assertEqual(pp, 13)
        self.assertEqual(final, 13.25)


if __name__ == "__main__":
    unittest.main()
