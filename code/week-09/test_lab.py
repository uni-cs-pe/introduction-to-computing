"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
MAX_GRADES = 100


def run(program, stdin=""):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20,
    )
    return done.stdout.strip(), done.returncode


def stats(average, largest, above):
    return f"Promedio: {average}\nMayor: {largest}\nSuperan el promedio: {above}"


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["addresses", "grades_stats", "dice", "out_of_bounds"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_addresses_step_by_element_size(self):
        out, status = run("addresses")
        self.assertEqual(status, 0)
        found = re.findall(r"^(int|char) (\d): 0x([0-9a-f]+)$", out, re.M)
        self.assertEqual(len(found), 10, out)
        sizes = {"int": 4, "char": 1}
        for kind, size in sizes.items():
            rows = [(int(i), int(a, 16)) for k, i, a in found if k == kind]
            self.assertEqual([i for i, _ in rows], [0, 1, 2, 3, 4])
            for (_, low), (_, high) in zip(rows, rows[1:]):
                with self.subTest(kind=kind):
                    self.assertEqual(high - low, size)

    def test_grades_stats_normal(self):
        cases = {
            "4 12 18 10 16": stats("14.00", 18, 2),
            "3 11 12 14": stats("12.33", 14, 1),
            "1 20": stats("20.00", 20, 0),
            "1 0": stats("0.00", 0, 0),
            "2 0 1": stats("0.50", 1, 1),
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(run("grades_stats", text), (expected, 0))

    def test_grade_equal_to_average_does_not_count(self):
        self.assertEqual(run("grades_stats", "3 10 10 10"), (stats("10.00", 10, 0), 0))
        self.assertEqual(run("grades_stats", "3 9 10 11"), (stats("10.00", 11, 1), 0))

    def test_largest_can_be_first_or_last(self):
        self.assertEqual(run("grades_stats", "3 20 1 3")[0], stats("8.00", 20, 1))
        self.assertEqual(run("grades_stats", "3 1 3 20")[0], stats("8.00", 20, 1))

    def test_grades_stats_full_array(self):
        text = f"{MAX_GRADES} " + " ".join(["15"] * (MAX_GRADES - 1) + ["20"])
        self.assertEqual(run("grades_stats", text), (stats("15.05", 20, 1), 0))

    def test_grades_stats_bad_count(self):
        for n in [0, -1, MAX_GRADES + 1, 1000000]:
            with self.subTest(n=n):
                self.assertEqual(run("grades_stats", f"{n} 10 10"), ("Cantidad fuera de rango", 1))

    def test_grades_stats_bad_input(self):
        for text in ["", "abc", "3 10 abc", "3 10 12"]:
            with self.subTest(text=text):
                self.assertEqual(run("grades_stats", text), ("Entrada inválida", 1))

    def test_grades_stats_bad_grade(self):
        for text in ["2 10 21", "2 -1 10"]:
            with self.subTest(text=text):
                self.assertEqual(run("grades_stats", text), ("Nota fuera de rango", 1))

    def test_dice_counts_add_up_and_are_near_the_expected_value(self):
        for seed in [1, 2, 2026]:
            with self.subTest(seed=seed):
                out, status = run("dice", str(seed))
                self.assertEqual(status, 0)
                found = re.findall(r"^Cara (\d): (\d+)$", out, re.M)
                self.assertEqual([face for face, _ in found], list("123456"), out)
                counts = [int(count) for _, count in found]
                self.assertEqual(sum(counts), 10000)
                # La desviación típica de cada cara es cercana a 37: 300 es muy holgado.
                for count in counts:
                    self.assertLess(abs(count - 10000 / 6), 300)

    def test_dice_seed_repeats_the_results(self):
        self.assertEqual(run("dice", "7"), run("dice", "7"))
        self.assertNotEqual(run("dice", "7"), run("dice", "8"))

    def test_dice_bad_seed(self):
        for text in ["", "abc"]:
            with self.subTest(text=text):
                self.assertEqual(run("dice", text), ("Entrada inválida", 1))

    def test_out_of_bounds_inside(self):
        for index in [0, 2, 4]:
            with self.subTest(index=index):
                self.assertEqual(run("out_of_bounds", str(index)), (f"values[{index}] = 99", 0))

    def test_out_of_bounds_bad_input(self):
        self.assertEqual(run("out_of_bounds", "abc"), ("Entrada inválida", 1))

    def test_out_of_bounds_is_seen_by_the_sanitizer(self):
        out, status = run("out_of_bounds", "5")
        self.assertIn("stack-buffer-overflow", out)
        self.assertNotEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
