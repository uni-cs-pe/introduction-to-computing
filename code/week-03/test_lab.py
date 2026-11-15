"""Pruebas del laboratorio 3. Corren sobre lab/ con `make test-lab`, y sobre solution/
dentro de `make test`, si esa carpeta existe. La actividad 5 (Git) no se prueba aquí:
se revisa en el laboratorio."""
import os
import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
SOURCE = HERE / LAB_DIR
BIN = HERE / "build" / LAB_DIR


def run(name, stdin=""):
    return subprocess.run([str(BIN / name)], input=stdin.encode(), capture_output=True, timeout=20)


def answers():
    values = {}
    for line in (SOURCE / "answers.txt").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            # Se aceptan mayúsculas, espacios y el prefijo 0x: c3 b1, C3B1, 0xca.
            values[key.strip()] = value.lower().replace(" ", "").replace("0x", "")
    return values


class Activity1(unittest.TestCase):
    def test_by_hand(self):
        self.assertEqual(answers().get("binario_202"), "11001010")
        self.assertEqual(answers().get("hexadecimal_202"), "ca")

    def test_program_uses_percent_x(self):
        self.assertRegex((SOURCE / "hex_202.c").read_text(encoding="utf-8"), r"%[0-9]*[xX]")
        self.assertEqual(run("hex_202").stdout.decode().strip().lower(), "ca")


class Activity2(unittest.TestCase):
    def test_normal_value(self):
        lines = run("int_overflow", "41\n").stdout.decode().strip().splitlines()
        self.assertTrue(lines, "el programa no escribió nada")
        self.assertEqual(lines[-1], "42")

    def test_overflow_message_and_line(self):
        stderr = run("int_overflow", "2147483647\n").stderr.decode()
        found = re.search(r"int_overflow\.c:(\d+):\d+: runtime error: signed integer overflow", stderr)
        self.assertIsNotNone(found, "no apareció el mensaje de overflow")
        self.assertEqual(answers().get("linea_overflow"), found.group(1))


class Activity3(unittest.TestCase):
    def test_twenty_decimals(self):
        self.assertIn("0.30000000000000004441", run("float_print").stdout.decode())


class Activity4(unittest.TestCase):
    def test_year_file(self):
        path = SOURCE / "year.txt"
        self.assertTrue(path.exists(), f"falta crear {LAB_DIR}/year.txt")
        data = path.read_bytes()
        self.assertIn(data, (b"a\xc3\xb1o\n", b"a\xc3\xb1o"), "year.txt debe contener año, en UTF-8")
        self.assertEqual(answers().get("bytes_year"), str(len(data)))

    def test_enye_bytes(self):
        self.assertEqual(answers().get("bytes_enye"), "c3b1")


if __name__ == "__main__":
    unittest.main()
