"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
EXACT = 1 / 6
# Tolerancias: 8 desviaciones típicas de la estimación, un margen muy amplio.
TOLERANCES = {100: 0.3, 10000: 0.03, 1000000: 0.003}


def run(program, stdin=""):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / program)], input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120,
    )
    return done.stdout, done.returncode


def primes_up_to(limit):
    return [n for n in range(2, limit + 1)
            if all(n % d != 0 for d in range(2, int(n ** 0.5) + 1))]


def parse_estimates(out):
    """Parte la salida en (intentos, estimación, error). Falla si no tiene la forma pedida."""
    rows = []
    for line in out.splitlines():
        match = re.fullmatch(r"(\d+) (\d\.\d{4}) (\d\.\d{4})", line)
        if not match:
            raise AssertionError(f"línea con otra forma: {line!r}")
        rows.append((int(match[1]), float(match[2]), float(match[3])))
    return rows


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class LabTests(unittest.TestCase):
    def test_no_warnings(self):
        for name in ["triangle", "primes", "dice_estimate"]:
            with self.subTest(name=name):
                done = subprocess.run(
                    ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
                     str(HERE / LAB_DIR / f"{name}.c")],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_triangle(self):
        for height in [1, 3, 5, 50]:
            expected = "".join("*" * row + "\n" for row in range(1, height + 1))
            with self.subTest(height=height):
                self.assertEqual(run("triangle", str(height)), (expected, 0))

    def test_triangle_rejects(self):
        for text in ["0", "-3", "51"]:
            with self.subTest(text=text):
                self.assertEqual(run("triangle", text), ("Altura fuera de rango\n", 1))
        for text in ["abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("triangle", text), ("Entrada inválida\n", 1))

    def test_primes(self):
        for limit in [1, 2, 3, 10, 49, 100, 1000, 10000]:
            expected = "".join(f"{p}\n" for p in primes_up_to(limit))
            with self.subTest(limit=limit):
                self.assertEqual(run("primes", str(limit)), (expected, 0))

    def test_primes_rejects(self):
        for text in ["0", "-7", "100001"]:
            with self.subTest(text=text):
                self.assertEqual(run("primes", text), ("N fuera de rango\n", 1))
        for text in ["abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("primes", text), ("Entrada inválida\n", 1))

    def test_estimates_have_the_form_and_stay_near(self):
        for seed in [1, 7, 42]:
            out, status = run("dice_estimate", str(seed))
            with self.subTest(seed=seed):
                self.assertEqual(status, 0)
                rows = parse_estimates(out)
                self.assertEqual([row[0] for row in rows], [100, 10000, 1000000])
                for trials, value, error in rows:
                    self.assertLess(abs(value - EXACT), TOLERANCES[trials])
                    self.assertAlmostEqual(error, abs(value - EXACT), delta=0.00011)

    def test_each_row_starts_again_with_one_seed(self):
        # Con un rand falso, todos los intentos suman 7: cada fila debe dar 1.0000. Si hits
        # no vuelve a 0, una fila da más que 1, y una segunda llamada a srand se nota.
        binary = HERE / "build" / LAB_DIR / "dice_estimate_fake"
        subprocess.run(["gcc", "-std=c17", "-w", str(HERE / LAB_DIR / "dice_estimate.c"),
                        str(HERE / "fake_rand.c"), "-o", str(binary), "-lm"], check=True)
        done = subprocess.run([str(binary)], input="42", text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=120)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual([row[1] for row in parse_estimates(done.stdout)], [1.0, 1.0, 1.0])

    def test_same_seed_same_output(self):
        self.assertEqual(run("dice_estimate", "42"), run("dice_estimate", "42"))

    def test_other_seed_other_output(self):
        self.assertNotEqual(run("dice_estimate", "1")[0], run("dice_estimate", "42")[0])

    def test_estimate_rejects(self):
        self.assertEqual(run("dice_estimate", "-1"), ("La semilla no puede ser negativa\n", 1))
        for text in ["abc", ""]:
            with self.subTest(text=text):
                self.assertEqual(run("dice_estimate", text), ("Entrada inválida\n", 1))


if __name__ == "__main__":
    unittest.main()
