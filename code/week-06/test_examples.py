"""Comprueba lo que los apuntes afirman sobre los programas de la semana 6.

Los números de rand dependen de la implementación de C. Por eso estas pruebas no
comparan valores aleatorios exactos: comprueban rangos y propiedades.
"""
import pathlib
import re
import subprocess
import tempfile
import time
import unittest

HERE = pathlib.Path(__file__).parent
BUILD = HERE / "build"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]
EXACT = 1 / 6
# Con n intentos, la desviación típica de la estimación es la raíz de
# (1/6)(5/6)/n: unas 0.00037 con 1000000 y 0.0037 con 10000. Las tolerancias son
# 8 veces eso, así que cualquier generador razonable las cumple.
TOLERANCE_1M = 0.003
TOLERANCE_10K = 0.03


def run(program, stdin=""):
    """Ejecuta un programa de build/; devuelve su salida (con errores) y su estado."""
    done = subprocess.run(
        [str(BUILD / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    return done.stdout, done.returncode


def compile_error_demo(name):
    """Compila un programa de errors/; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / name
    done = subprocess.run(
        ["gcc", *FLAGS, f"errors/{name}.c", "-o", str(out)], cwd=HERE,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return done.stdout, done.returncode, out


def run_demo(binary):
    done = subprocess.run(
        [str(binary)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    return done.stdout


def estimate(seed, trials):
    out, status = run("dice_seven", f"{seed} {trials}")
    assert status == 0, out
    match = re.fullmatch(r"(\d+) intentos, (\d+) sumaron 7, estimación (\d\.\d{4})\n", out)
    assert match, out
    return int(match[1]), int(match[2]), float(match[3])


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)


class NestedLoops(unittest.TestCase):
    def test_rectangle_shape(self):
        for rows, cols in [(1, 1), (2, 5), (4, 3)]:
            with self.subTest(rows=rows, cols=cols):
                self.assertEqual(run("rectangle", f"{rows} {cols}"), (("*" * cols + "\n") * rows, 0))

    def test_rectangle_rejects(self):
        self.assertEqual(run("rectangle", "abc"), ("Entrada inválida\n", 1))
        self.assertEqual(run("rectangle", "2"), ("Entrada inválida\n", 1))
        self.assertEqual(run("rectangle", "0 5"), ("Filas y columnas deben ser positivas\n", 1))

    def test_times_table(self):
        for n in [1, 3, 12]:
            expected = "".join(
                "".join(f"{r * c:4d}" for c in range(1, n + 1)) + "\n" for r in range(1, n + 1)
            )
            with self.subTest(n=n):
                self.assertEqual(run("times_table", str(n)), (expected, 0))

    def test_times_table_limits(self):
        for text in ["0", "13"]:
            self.assertEqual(run("times_table", text), ("n debe estar entre 1 y 12\n", 1))

    def test_count_formulas(self):
        for n in [1, 3, 10, 20, 100, 200, 5000]:
            out, status = run("count_runs", str(n))
            numbers = [int(x) for x in re.findall(r": (\d+)", out)]
            with self.subTest(n=n):
                self.assertEqual(status, 0)
                self.assertEqual(numbers, [n, n * n, n * (n + 1) // 2])

    def test_count_rejects_what_could_overflow(self):
        self.assertEqual(run("count_runs", "5001"), ("n debe estar entre 1 y 5000\n", 1))
        self.assertLess(5000 * 5000, 2 ** 31)

    def test_doubling_quadruples(self):
        for n in [10, 100]:
            small = [int(x) for x in re.findall(r": (\d+)", run("count_runs", str(n))[0])]
            big = [int(x) for x in re.findall(r": (\d+)", run("count_runs", str(2 * n))[0])]
            self.assertEqual(big[1], 4 * small[1])
            self.assertAlmostEqual(big[2] / small[2], 4, delta=0.2)

    def test_staircase(self):
        expected = "".join(
            "".join(f"{c:3d}" for c in range(1, r + 1)) + "\n" for r in range(1, 5)
        )
        self.assertEqual(run("staircase", "4"), (expected, 0))

    def test_divisors(self):
        expected = ""
        for n in range(1, 101):
            found = [d for d in range(1, n + 1) if n % d == 0]
            expected += f"{n}: {' '.join(map(str, found))} ({len(found)})\n"
        self.assertEqual(run("divisors", "100"), (expected, 0))

    def test_divisor_counts_show_the_primes(self):
        out, _ = run("divisors", "12")
        twos = [int(line.split(":")[0]) for line in out.splitlines() if line.endswith("(2)")]
        self.assertEqual(twos, [2, 3, 5, 7, 11])


class NestedErrors(unittest.TestCase):
    def test_same_counter_makes_one_row(self):
        messages, status, binary = compile_error_demo("same_counter")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(run_demo(binary), "***\n")

    def test_no_reset_leaves_empty_rows(self):
        messages, status, binary = compile_error_demo("no_reset")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(run_demo(binary), "****\n\n\n")

    def test_missing_stdlib_does_not_compile(self):
        messages, status, _ = compile_error_demo("no_stdlib")
        self.assertNotEqual(status, 0)
        self.assertIn("implicit declaration of function", messages)


class ToyGenerator(unittest.TestCase):
    def test_every_seed_has_period_16(self):
        for seed in range(16):
            out, status = run("toy_generator", str(seed))
            numbers = [int(x) for x in out.split()]
            with self.subTest(seed=seed):
                self.assertEqual(status, 0)
                self.assertEqual(sorted(numbers[:16]), list(range(16)))
                self.assertEqual(numbers[15], seed)
                self.assertEqual(numbers[16:], numbers[:2])

    def test_rejects_other_seeds(self):
        self.assertEqual(run("toy_generator", "16"), ("La semilla debe estar entre 0 y 15\n", 1))


class Rand(unittest.TestCase):
    def test_rand_max_is_allowed_and_values_fit(self):
        out, status = run("rand_max")
        lines = out.splitlines()
        rand_max = int(lines[0].split("= ")[1])
        self.assertEqual(status, 0)
        self.assertGreaterEqual(rand_max, 32767)
        for value in lines[1:]:
            self.assertTrue(0 <= int(value) <= rand_max)

    def test_no_srand_is_seed_1(self):
        without_srand = run("rand_max")[0].splitlines()[1:]
        self.assertEqual(without_srand, run("seed", "1")[0].splitlines())

    def test_same_seed_same_sequence(self):
        for seed in [0, 1, 42, 2000]:
            with self.subTest(seed=seed):
                self.assertEqual(run("seed", str(seed)), run("seed", str(seed)))

    def test_other_seed_other_sequence(self):
        self.assertNotEqual(run("seed", "1")[0], run("seed", "42")[0])

    def test_seed_rejects(self):
        self.assertEqual(run("seed", "-1"), ("La semilla no puede ser negativa\n", 1))
        self.assertEqual(run("seed", "abc"), ("Entrada inválida\n", 1))

    def test_time_seed_is_a_die(self):
        out, status = run("time_seed")
        self.assertEqual(status, 0)
        values = [int(x) for x in out.split()]
        self.assertEqual(len(values), 10)
        self.assertTrue(all(1 <= v <= 6 for v in values))

    def test_same_second_same_output(self):
        # Puede tocar justo el cambio de segundo: basta que coincidan en un intento.
        for _ in range(5):
            if run("time_seed") == run("time_seed"):
                return
        self.fail("dos corridas seguidas nunca coincidieron")

    def test_other_second_other_output(self):
        first = run("time_seed")[0]
        time.sleep(1.1)
        self.assertNotEqual(first, run("time_seed")[0])

    def test_srand_in_loop_repeats(self):
        _, status, binary = compile_error_demo("srand_in_loop")
        self.assertEqual(status, 0)
        values = run_demo(binary).split()
        self.assertEqual(len(values), 10)
        # Dos valores como máximo, por si el segundo cambia durante la corrida.
        self.assertLessEqual(len(set(values)), 2)


class Range(unittest.TestCase):
    def test_values_in_range_for_many_seeds(self):
        for low, high in [(1, 6), (0, 20), (-5, 5), (7, 7), (-10000, 10000)]:
            for seed in range(30):
                out, status = run("range", f"{low} {high} {seed}")
                with self.subTest(low=low, high=high, seed=seed):
                    self.assertEqual(status, 0)
                    values = [int(x) for x in out.split()]
                    self.assertEqual(len(values), 10)
                    self.assertTrue(all(low <= v <= high for v in values))

    def test_die_reaches_both_ends(self):
        seen = set()
        for seed in range(30):
            seen.update(int(x) for x in run("range", f"1 6 {seed}")[0].split())
        self.assertEqual(seen, {1, 2, 3, 4, 5, 6})

    def test_rejects(self):
        self.assertEqual(run("range", "6 1 42"), ("Rango inválido\n", 1))
        self.assertEqual(run("range", "-10001 0 42"), ("Rango inválido\n", 1))
        self.assertEqual(run("range", "0 10001 42"), ("Rango inválido\n", 1))
        self.assertEqual(run("range", "1 6 -1"), ("La semilla no puede ser negativa\n", 1))
        self.assertEqual(run("range", "1 6"), ("Entrada inválida\n", 1))

    def test_forgetting_the_one(self):
        _, status, binary = compile_error_demo("die_off_by_one")
        self.assertEqual(status, 0)
        self.assertEqual(run_demo(binary), "Menor: 0\nMayor: 5\n")

    def test_die_counts_add_up_and_stay_near(self):
        out, status = run("die_counts", "42 600000")
        counts = [int(x) for x in re.findall(r"Cara \d: (\d+)", out)]
        self.assertEqual(status, 0)
        self.assertEqual(sum(counts), 600000)
        # 100000 esperados, con desviación típica cerca de 289.
        for count in counts:
            self.assertLess(abs(count - 100000), 1000)

    def test_die_counts_rejects(self):
        self.assertEqual(run("die_counts", "42 0"),
                         ("Los lanzamientos deben estar entre 1 y 10000000\n", 1))

    def test_bias_arithmetic_in_the_notes(self):
        values = 2 ** 31
        self.assertEqual(values // 6, 357913941)
        self.assertEqual(values % 6, 2)
        self.assertEqual([sum(1 for v in range(8) if v % 6 == r) for r in range(6)],
                         [2, 2, 1, 1, 1, 1])


class Dice(unittest.TestCase):
    def test_exact_counts(self):
        out, status = run("dice_exact")
        self.assertEqual(status, 0)
        lines = out.splitlines()
        self.assertEqual(len(lines), 11)
        total = 0
        for target, line in zip(range(2, 13), lines):
            ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == target)
            total += ways
            self.assertEqual(line, f"Suma {target:2d}: {ways} de 36, {ways / 36:.4f}")
        self.assertEqual(total, 36)

    def test_estimate_is_consistent(self):
        for seed, trials in [(42, 100), (7, 100), (1, 10000)]:
            shown, hits, value = estimate(seed, trials)
            with self.subTest(seed=seed, trials=trials):
                self.assertEqual(shown, trials)
                self.assertTrue(0 <= hits <= trials)
                self.assertAlmostEqual(value, hits / trials, delta=0.00006)

    def test_same_seed_same_estimate(self):
        self.assertEqual(estimate(42, 10000), estimate(42, 10000))

    def test_tolerances(self):
        for seed in [1, 2, 3, 7, 42]:
            with self.subTest(seed=seed):
                self.assertLess(abs(estimate(seed, 10000)[2] - EXACT), TOLERANCE_10K)
                self.assertLess(abs(estimate(seed, 1000000)[2] - EXACT), TOLERANCE_1M)

    def test_error_falls_with_more_trials(self):
        worst = [max(abs(estimate(seed, trials)[2] - EXACT) for seed in [1, 2, 3, 7, 42])
                 for trials in [100, 10000, 1000000]]
        self.assertGreater(worst[0], worst[1])
        self.assertGreater(worst[1], worst[2])

    def test_rejects(self):
        message = "Los intentos deben estar entre 1 y 10000000\n"
        self.assertEqual(run("dice_seven", "42 0"), (message, 1))
        self.assertEqual(run("dice_seven", "42 10000001"), (message, 1))
        self.assertEqual(run("dice_seven", "-1 100"), ("La semilla no puede ser negativa\n", 1))
        self.assertEqual(run("dice_seven", "abc"), ("Entrada inválida\n", 1))

    def test_integer_division_gives_zero(self):
        messages, status, binary = compile_error_demo("int_probability")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(run_demo(binary), "Estimación: 0.0000\n")


if __name__ == "__main__":
    unittest.main()
