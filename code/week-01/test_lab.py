"""Pruebas del laboratorio 1. Corren sobre lab/ con `make test-lab`, y sobre
solution/ dentro de `make test`."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

# Muestra solo el mensaje de cada prueba, sin el detalle interno de Python.
__unittest = True

HERE = Path(__file__).resolve().parent
LAB_DIR = os.environ.get("LAB_DIR", "solution")
LAB = HERE / LAB_DIR


class HolaTest(unittest.TestCase):
    longMessage = False

    def test_folder_exists(self):
        self.assertTrue((LAB / "lab01").is_dir(),
                        f"No existe la carpeta {LAB_DIR}/lab01. Créenla con mkdir.")

    def test_hola_compiles_and_greets(self):
        source = LAB / "lab01" / "hola.c"
        self.assertTrue(source.is_file(), f"No existe {LAB_DIR}/lab01/hola.c.")
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "hola"
            gcc = subprocess.run(
                ["gcc", "-Wall", "-Wextra", "-Werror", "-std=c17", str(source), "-o", str(exe)],
                capture_output=True, text=True)
            self.assertEqual(gcc.returncode, 0, "hola.c no compila sin advertencias:\n" + gcc.stderr)
            run = subprocess.run([str(exe)], capture_output=True, text=True, timeout=5)
        self.assertEqual(run.stdout, "Hola, mundo\n", "hola debe escribir exactamente: Hola, mundo")
        self.assertEqual(run.returncode, 0, "main debe terminar con return 0")


class NotesTest(unittest.TestCase):
    longMessage = False

    def read(self, name):
        path = LAB / name
        self.assertTrue(path.is_file(), f"No existe {LAB_DIR}/{name}.")
        text = path.read_text(encoding="utf-8")
        self.assertNotIn("___", text, f"A {name} le faltan espacios por completar (___).")
        return text

    def test_errors_file(self):
        text = self.read("compiler_errors.txt")
        for fragment in ("expected", "missing terminating"):
            self.assertIn(fragment, text, f"Copien en compiler_errors.txt el mensaje de gcc ({fragment}...).")

    def test_change_file(self):
        text = self.read("change.txt")
        start, end = text.index("algoritmo dar_vuelto"), text.index("fin algoritmo")
        for word in ("mientras", "←", "≥", "fin mientras", "escribir"):
            self.assertIn(word, text[start:end], f"El pseudocódigo debe usar: {word}")
        position = text.index("Seguimiento")
        for value in ("780", "280", "80", "30", "10", "0"):
            found = text.find(value, position)
            self.assertNotEqual(found, -1, f"La tabla debe pasar por el valor {value}.")
            position = found + len(value)
        self.assertIn("Total de monedas: 5", text)


if __name__ == "__main__":
    unittest.main()
