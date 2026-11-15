"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")


def run(program, stdin):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def run_with_file(program, name):
    with open(HERE / "lab" / name, encoding="utf-8") as data:
        done = subprocess.run(
            [str(HERE / "build" / LAB_DIR / program)], stdin=data, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
        )
    return done.stdout, done.returncode


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["sum_until_zero", "is_prime", "count_lines", "validate_grade"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_sum_average_max(self):
        cases = {
            "10 15 5 0": ("Suma: 30\nPromedio: 10.00\nMayor: 15\n"),
            "7 0": ("Suma: 7\nPromedio: 7.00\nMayor: 7\n"),
            "-5 -2 -9 0": ("Suma: -16\nPromedio: -5.33\nMayor: -2\n"),
            "1 2 0": ("Suma: 3\nPromedio: 1.50\nMayor: 2\n"),
            "3\n4\n0\n99\n": ("Suma: 7\nPromedio: 3.50\nMayor: 4\n"),
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("sum_until_zero", text), (expected, 0))

    def test_sum_no_data(self):
        self.assertEqual(run("sum_until_zero", "0"), ("Sin datos\n", 0))

    def test_sum_bad_input(self):
        for text in ["", "abc", "4 abc", "4 5", "4 5 x 0"]:
            with self.subTest(text=text):
                self.assertEqual(run("sum_until_zero", text), ("Entrada inválida\n", 1))

    def test_primes(self):
        for n in [2, 3, 5, 7, 11, 13, 97, 7919, 2147483647]:
            with self.subTest(n=n):
                self.assertEqual(run("is_prime", str(n)), ("Primo\n", 0))

    def test_not_primes(self):
        for n in [-7, -1, 0, 1, 4, 6, 9, 15, 25, 49, 121, 2147483646, 2147395600]:
            with self.subTest(n=n):
                self.assertEqual(run("is_prime", str(n)), ("No primo\n", 0))

    def test_prime_bad_input(self):
        for text in ["abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("is_prime", text), ("Entrada inválida\n", 1))

    def test_count_lines_from_files(self):
        self.assertEqual(run_with_file("count_lines", "three_lines.txt"), ("3\n", 0))
        self.assertEqual(run_with_file("count_lines", "no_final_newline.txt"), ("2\n", 0))
        self.assertEqual(run_with_file("count_lines", "empty.txt"), ("0\n", 0))

    def test_count_lines_other_inputs(self):
        self.assertEqual(run("count_lines", "\n\n\n\n"), ("4\n", 0))
        self.assertEqual(run("count_lines", "ñandú\n"), ("1\n", 0))

    def test_count_lines_with_byte_0xff(self):
        # Un byte 0xFF no es EOF. Con c de tipo char, esta prueba falla.
        done = subprocess.run(
            [str(HERE / "build" / LAB_DIR / "count_lines")], input=b"a\xffb\nc\n",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
        )
        self.assertEqual(done.stdout, b"2\n")

    def test_validate_grade(self):
        cases = {
            "15": "Nota válida: 15\n",
            "0": "Nota válida: 0\n",
            "20": "Nota válida: 20\n",
            "25 -1 20": "Nota fuera de rango\nNota fuera de rango\nNota válida: 20\n",
            "21 7 30": "Nota fuera de rango\nNota válida: 7\n",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("validate_grade", text), (expected, 0))

    def test_validate_grade_bad_input(self):
        self.assertEqual(run("validate_grade", "abc"), ("Entrada inválida\n", 1))
        self.assertEqual(run("validate_grade", ""), ("Entrada inválida\n", 1))
        self.assertEqual(run("validate_grade", "25"), ("Nota fuera de rango\nEntrada inválida\n", 1))
        self.assertEqual(run("validate_grade", "25 abc"), ("Nota fuera de rango\nEntrada inválida\n", 1))


if __name__ == "__main__":
    unittest.main()
