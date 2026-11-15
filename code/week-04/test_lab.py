"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
PASSING_GRADE = 11


def run(program, stdin):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout.strip(), done.returncode


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["grade", "leap_year", "calculator"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_grade_passes_and_fails(self):
        cases = {0: "Desaprobado", PASSING_GRADE - 1: "Desaprobado",
                 PASSING_GRADE: "Aprobado", 20: "Aprobado"}
        for grade, text in cases.items():
            with self.subTest(grade=grade):
                self.assertEqual(run("grade", str(grade)), (text, 0))

    def test_grade_out_of_range(self):
        for grade in [-1, 21, 100]:
            with self.subTest(grade=grade):
                self.assertEqual(run("grade", str(grade)), ("Nota fuera de rango", 1))

    def test_grade_not_a_number(self):
        for text in ["abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("grade", text), ("Entrada inválida", 1))

    def test_leap_years(self):
        cases = {1900: "No bisiesto", 2000: "Bisiesto", 2024: "Bisiesto", 2026: "No bisiesto",
                 2100: "No bisiesto", 2400: "Bisiesto", 2023: "No bisiesto"}
        for year, text in cases.items():
            with self.subTest(year=year):
                self.assertEqual(run("leap_year", str(year)), (text, 0))

    def test_leap_year_not_a_number(self):
        self.assertEqual(run("leap_year", "abc"), ("Entrada inválida", 1))

    def test_calculator_operations(self):
        cases = {"8 + 2": "10.00", "8 - 2": "6.00", "8 * 2": "16.00", "8 / 2": "4.00",
                 "7 / 2": "3.50", "0.1 + 0.2": "0.30", "8+2": "10.00", "0 / 5": "0.00"}
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("calculator", text), (expected, 0))

    def test_calculator_division_by_zero(self):
        for text in ["5 / 0", "5 / 0.0", "0 / 0"]:
            with self.subTest(text=text):
                self.assertEqual(run("calculator", text), ("Error: división entre 0", 1))

    def test_calculator_unknown_operator(self):
        self.assertEqual(run("calculator", "8 x 2"), ("Operador desconocido", 1))

    def test_calculator_bad_input(self):
        for text in ["abc", "8 /", "8 / abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("calculator", text), ("Entrada inválida", 1))


if __name__ == "__main__":
    unittest.main()
