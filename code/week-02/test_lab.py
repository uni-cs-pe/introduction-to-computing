"""Pruebas del laboratorio. Corren sobre lab/ con `make test-lab`, y sobre
solution/ dentro de `make test`, si esa carpeta existe."""
import os
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
FOLDER = HERE / LAB_DIR
BIN = HERE / "build" / LAB_DIR


def run(name, stdin=""):
    result = subprocess.run([str(BIN / name)], input=stdin, capture_output=True,
                            text=True, timeout=20)
    return result.stdout


@unittest.skipUnless(FOLDER.is_dir(), f"no existe {LAB_DIR}/")
class Lab(unittest.TestCase):
    def test_1_celsius(self):
        # 37 descubre la división entera: 9 / 5 daría 1 y el resultado sería 69.00.
        cases = {"100": "212.00", "0": "32.00", "-40": "-40.00", "37": "98.60",
                 "36.6": "97.88"}
        for given, expected in cases.items():
            with self.subTest(celsius=given):
                self.assertEqual(run("celsius", given + "\n"), expected + "\n")

    def test_2_predict_program(self):
        self.assertEqual(run("predict"),
                         "7 / 2 = 3\n7 % 2 = 1\n7.0 / 2 = 3.5\n(double) 7 / 2 = 3.5\n")

    def test_2_predictions_match_the_program(self):
        predictions = (FOLDER / "predictions.txt").read_text(encoding="utf-8")
        self.assertNotIn("?", predictions, "falta completar predictions.txt")
        self.assertEqual(predictions, run("predict"))

    def test_3_time_split(self):
        cases = {"3725": "1 h 2 min 5 s", "0": "0 h 0 min 0 s", "59": "0 h 0 min 59 s",
                 "3600": "1 h 0 min 0 s", "86399": "23 h 59 min 59 s",
                 "90061": "25 h 1 min 1 s"}
        for given, expected in cases.items():
            with self.subTest(seconds=given):
                self.assertEqual(run("time_split", given + "\n"), expected + "\n")

    def test_4_redirect(self):
        entrada = FOLDER / "entrada.txt"
        salida = FOLDER / "salida.txt"
        self.assertTrue(entrada.exists(), f"falta {LAB_DIR}/entrada.txt")
        self.assertTrue(salida.exists(), f"falta {LAB_DIR}/salida.txt")
        self.assertEqual(salida.read_text(encoding="utf-8"),
                         run("time_split", entrada.read_text(encoding="utf-8")))

    def test_5_type_sizes(self):
        self.assertIn("sizeof", (FOLDER / "type_sizes.c").read_text(encoding="utf-8"))
        self.assertEqual(run("type_sizes"),
                         "int: 4 bytes\ndouble: 8 bytes\nchar: 1 bytes\n")


if __name__ == "__main__":
    unittest.main()
