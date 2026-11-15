"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution.

Las funciones se llaman directamente: cada prueba compila el archivo del laboratorio
junto con un main propio, sin correr el main de ustedes.
"""
import os
import pathlib
import re
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
FLAGS = ["-Wall", "-Wextra", "-std=c17", "-g", "-fsanitize=address,undefined"]


def run(program, stdin=""):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout.strip(), done.returncode


def source(name):
    return (HERE / LAB_DIR / f"{name}.c").read_text(encoding="utf-8")


def call_with_driver(name, driver_main, stdin):
    """Compila lab/<name>.c con otro main y devuelve lo que escribe."""
    folder = pathlib.Path(tempfile.mkdtemp())
    driver = folder / "driver.c"
    driver.write_text(
        f'#define main lab_main\n#include "{HERE / LAB_DIR / name}.c"\n#undef main\n{driver_main}\n',
        encoding="utf-8",
    )
    binary = folder / "driver"
    built = subprocess.run(
        ["gcc", *FLAGS, str(driver), "-o", str(binary)],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if built.returncode != 0:
        raise AssertionError(f"No compila con las funciones pedidas:\n{built.stdout}")
    done = subprocess.run(
        [str(binary)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20,
    )
    return done.stdout


def one_argument_main(function):
    return (
        "int main(void) {\n    int n;\n    while (scanf(\"%d\", &n) == 1) {\n"
        f"        printf(\"%d\\n\", {function}(n));\n    }}\n    return 0;\n}}"
    )


def prime(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))


def leap(y):
    return (y % 4 == 0 and y % 100 != 0) or y % 400 == 0


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["functions", "grades_bug", "adder4"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    # Parte 1
    def test_is_prime_edges(self):
        values = [-7, -2, -1, 0, 1, 2, 3, 4, 9, 25, 49, 121, 169, 997, 1000, 1001, 7919, 1000003, 2147483647]
        output = call_with_driver("functions", one_argument_main("is_prime"), " ".join(map(str, values)))
        for value, line in zip(values, output.split()):
            with self.subTest(n=value):
                self.assertEqual(int(line), int(prime(value)))
        self.assertEqual(len(output.split()), len(values), output)

    def test_is_prime_first_numbers(self):
        values = list(range(-20, 300))
        output = call_with_driver("functions", one_argument_main("is_prime"), " ".join(map(str, values)))
        self.assertEqual([int(x) for x in output.split()], [int(prime(n)) for n in values])

    def test_is_leap_year(self):
        values = [1900, 2000, 2023, 2024, 2026, 2100, 2400, 1600, 1996, 1999]
        output = call_with_driver("functions", one_argument_main("is_leap_year"), " ".join(map(str, values)))
        self.assertEqual([int(x) for x in output.split()], [int(leap(y)) for y in values])

    def test_their_tests_exist_and_pass(self):
        text = source("functions")
        self.assertNotIn("NDEBUG", text)
        prime_tests = re.findall(r"^\s*assert\(is_prime\(", text, re.M)
        leap_tests = re.findall(r"^\s*assert\(is_leap_year\(", text, re.M)
        self.assertGreaterEqual(len(prime_tests), 6, "faltan pruebas de is_prime")
        self.assertGreaterEqual(len(leap_tests), 4, "faltan pruebas de is_leap_year")
        self.assertEqual(run("functions"), ("Todas las pruebas pasaron", 0))

    # Parte 2
    def test_grades(self):
        cases = {"4\n12 8 11 15\n": "Promedio: 11.50\nAprobados: 3",
                 "1\n20\n": "Promedio: 20.00\nAprobados: 1",
                 "2\n11 10\n": "Promedio: 10.50\nAprobados: 1",
                 "3\n0 0 1\n": "Promedio: 0.33\nAprobados: 0",
                 "2\n10 11\n": "Promedio: 10.50\nAprobados: 1"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("grades_bug", text), (expected, 0))

    def test_grades_input_file(self):
        text = (HERE / "lab" / "grades.txt").read_text(encoding="utf-8")
        self.assertEqual(run("grades_bug", text), ("Promedio: 11.50\nAprobados: 3", 0))

    def test_grades_bad_input(self):
        cases = {"abc": "Cantidad inválida", "0": "Cantidad inválida", "-2": "Cantidad inválida",
                 "2\n21 3": "Nota inválida", "2\n-1 3": "Nota inválida", "2\n5": "Nota inválida",
                 "2\nabc": "Nota inválida"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("grades_bug", text), (expected, 1))

    # Parte 4
    def test_adder_functions(self):
        driver = (
            "int main(void) {\n    int a, b, c;\n"
            "    while (scanf(\"%d %d %d\", &a, &b, &c) == 3) {\n"
            "        printf(\"%d %d\\n\", sum_bit(a, b, c), carry_bit(a, b, c));\n    }\n"
            "    return 0;\n}"
        )
        triples = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
        stdin = "\n".join(f"{a} {b} {c}" for a, b, c in triples)
        lines = call_with_driver("adder4", driver, stdin).splitlines()
        expected = [f"{(a + b + c) % 2} {(a + b + c) // 2}" for a, b, c in triples]
        self.assertEqual(lines, expected)

    def test_adder_no_longer_repeats(self):
        text = source("adder4")
        for name in ["partial0", "partial1", "partial2", "partial3"]:
            with self.subTest(name=name):
                self.assertNotIn(name, text)

    def test_adder_same_output(self):
        for a in range(16):
            for b in range(16):
                carries = []
                carry = 0
                total = 0
                for i in range(4):
                    bit_sum = (a >> i & 1) + (b >> i & 1) + carry
                    carry = bit_sum // 2
                    carries.append(carry)
                    total |= (bit_sum % 2) << i
                expected = ("acarreos: " + " ".join(str(c) for c in reversed(carries)) +
                            f"\nsuma:     {total:04b}")
                with self.subTest(a=a, b=b):
                    self.assertEqual(run("adder4", f"{a:04b} {b:04b}"), (expected, 0))

    def test_adder_bad_input(self):
        self.assertEqual(run("adder4", "abc"), ("Entrada inválida", 1))
        self.assertEqual(run("adder4", "0102 0011"), ("Los bits deben ser 0 o 1", 1))


if __name__ == "__main__":
    unittest.main()
