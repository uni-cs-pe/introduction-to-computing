"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")


def run(program, *args, stdin=""):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program), *args], input=stdin, encoding="utf-8",
        errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    return done.stdout, done.returncode


def without_comments(path):
    return re.sub(r"//[^\n]*", "", path.read_text(encoding="utf-8"))


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def check(self, program, part):
        output, code = run(program, part)
        self.assertEqual(code, 0, output)

    def test_no_warnings(self):
        for name in ["searching", "sorting"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_searching_prints_the_table(self):
        output, code = run("searching")
        self.assertEqual(code, 0, output)
        self.assertEqual(output, "1000 1000 10\n10000 10000 14\n100000 100000 17\n"
                                 "Todas las pruebas pasaron\n")

    def test_linear_search(self):
        self.check("check_searching", "linear")

    def test_binary_search(self):
        self.check("check_searching", "binary")

    def test_linear_count(self):
        self.check("check_searching", "linear_count")

    def test_binary_count(self):
        self.check("check_searching", "binary_count")

    def test_mid_does_not_add_low_and_high(self):
        code = without_comments(HERE / LAB_DIR / "searching.c")
        self.assertNotRegex(code, r"\blow\s*\+\s*high\b")
        self.assertNotRegex(code, r"\bhigh\s*\+\s*low\b")

    def test_selection_sort(self):
        self.check("check_sorting", "sort")

    def test_is_sorted(self):
        self.check("check_sorting", "is_sorted")

    def test_seconds_selection_with_a_fake_clock(self):
        self.check("check_sorting", "seconds_selection")

    def test_seconds_qsort_with_a_fake_clock(self):
        self.check("check_sorting", "seconds_qsort")

    def test_count_does_not_fit_in_int(self):
        self.check("check_sorting_fast", "big_count")

    def test_sorting_program(self):
        # Solo la forma de la salida: los tiempos dependen de la máquina.
        output, code = run("sorting", stdin="10 100\n")
        self.assertEqual(code, 0, output)
        self.assertRegex(output, r"\A10 \d+\.\d{4} \d+\.\d{4} ordenado\n"
                                 r"100 \d+\.\d{4} \d+\.\d{4} ordenado\n\Z")


if __name__ == "__main__":
    unittest.main()
