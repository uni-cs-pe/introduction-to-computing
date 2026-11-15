"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution.

Se prueban dos cosas: que las funciones de suspect.c estén corregidas, y que las pruebas
de tests.c sirvan. Una prueba sirve si pasa con el código corregido y falla con el original.
"""
import os
import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
GROUPS = {"prime": "is_prime", "max": "max_of_array", "copy": "copy_text"}


def run(program, *args):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program), *args], encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def answer(*args):
    output, code = run("check_suspect", *args)
    # El programa se detiene con un informe si la función se sale del arreglo.
    return output.strip() if code == 0 else f"falló con estado {code}"


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class FixedFunctions(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["suspect", "tests"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_is_prime(self):
        cases = {-7: 0, 0: 0, 1: 0, 2: 1, 3: 1, 4: 0, 5: 1, 9: 0, 13: 1, 15: 0, 25: 0,
                 49: 0, 97: 1, 121: 0, 169: 0, 361: 0, 1369: 0, 7919: 1}
        for n, expected in cases.items():
            with self.subTest(n=n):
                self.assertEqual(answer("prime", str(n)), str(expected))

    def test_max_of_array(self):
        cases = [(["5"], "5"), (["-5"], "-5"), (["0"], "0"), (["14", "9", "17"], "17"),
                 (["20", "9", "17"], "20"), (["9", "20", "17"], "20"), (["-4", "-2", "-9"], "-2"),
                 (["-1", "-1"], "-1"), (["-9", "0", "-3"], "0"), (["3", "3", "3"], "3")]
        for numbers, expected in cases:
            with self.subTest(numbers=numbers):
                self.assertEqual(answer("max", *numbers), expected)

    def test_copy_text(self):
        cases = [("5", "hola", "[hola]"), ("5", "", "[]"), ("5", "luna!", "[luna]"),
                 ("5", "estrella", "[estr]"), ("3", "hola", "[ho]"), ("3", "ab", "[ab]"),
                 ("3", "abc", "[ab]"), ("2", "xy", "[x]"), ("1", "hola", "[]"), ("1", "", "[]")]
        for size, text, expected in cases:
            with self.subTest(size=size, text=text):
                self.assertEqual(answer("copy", size, text), expected)


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class YourTests(unittest.TestCase):
    def test_your_program_passes(self):
        output, code = run("tests")
        self.assertEqual((output, code), ("Todas las pruebas pasaron\n", 0),
                         "sus pruebas deben pasar con su suspect.c corregido")

    def test_each_group_passes_on_your_fixed_code(self):
        for group, name in GROUPS.items():
            with self.subTest(function=name):
                output, code = run("tests_fixed", group)
                self.assertEqual(code, 0, f"sus pruebas de {name} fallan con su código:\n{output}")

    def test_each_group_finds_the_bug_of_the_original(self):
        for group, name in GROUPS.items():
            with self.subTest(function=name):
                _, code = run("tests_original", group)
                self.assertNotEqual(
                    code, 0, f"sus pruebas de {name} pasan con el original, que tiene un bug")


if __name__ == "__main__":
    unittest.main()
