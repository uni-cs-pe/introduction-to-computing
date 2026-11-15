"""Vuelve a correr los comandos que aparecen en los apuntes y en las diapositivas
y comprueba que el código citado existe de verdad en esta carpeta."""
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
NOTES = ROOT / "notes" / "week-15.md"
SLIDES = ROOT / "slides" / "week-15.tex"
# En esta salida, solo las comillas de gcc cambian según el idioma del entorno.


def normalize(text):
    return text.replace("‘", "'").replace("’", "'")


def run_shell(command):
    done = subprocess.run(
        ["bash", "-c", command], cwd=HERE, encoding="utf-8", errors="replace",
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    return normalize(done.stdout)


def split_commands(lines):
    """Parte un bloque de terminal en pares (comando, líneas de salida)."""
    pairs = []
    for line in lines:
        if line.startswith("$ "):
            pairs.append((line[2:], []))
        elif pairs:
            pairs[-1][1].append(normalize(line.rstrip()))
    return pairs


def note_blocks(language):
    """Devuelve las líneas de cada bloque de los apuntes."""
    blocks, current = [], None
    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^> ?", "", raw)
        if current is None:
            if line.strip() == "```" + language:
                current = []
        elif line.strip() == "```":
            blocks.append(current)
            current = None
        else:
            current.append(line)
    return blocks


def slide_blocks(environments):
    text = SLIDES.read_text(encoding="utf-8")
    pattern = r"\\begin\{(?:%s)\}[^\n]*\n(.*?)\\end\{(?:%s)\}" % (environments, environments)
    return [match.group(1).splitlines() for match in re.finditer(pattern, text, re.S)]


def known_code_lines():
    lines = set()
    for source in list(HERE.glob("*.c")) + list((HERE / "errors").glob("*.c")):
        lines.update(line.strip() for line in source.read_text(encoding="utf-8").splitlines())
    return lines


class NotesAreTrue(unittest.TestCase):
    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_terminal_blocks_in_notes(self):
        checked = 0
        for lines in note_blocks("text"):
            if not lines or not lines[0].startswith("$ "):
                continue
            for command, expected in split_commands(lines):
                actual = run_shell(command).rstrip("\n")
                checked += 1
                with self.subTest(command=command):
                    output = [line.rstrip() for line in actual.split("\n")]
                    self.assertEqual("\n".join(output).strip(), "\n".join(expected).strip())
        self.assertGreater(checked, 5)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_code_blocks_in_notes_exist(self):
        known = known_code_lines()
        for lines in note_blocks("c"):
            for line in lines:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_tables_match_the_program(self):
        text = NOTES.read_text(encoding="utf-8")
        output = run_shell("build/spam_models")
        rows = {"Regla a mano (`u = 2`)": "Regla a mano", "Umbral aprendido (`u = 4`)": "Umbral aprendido",
                "Memorizador": "Memorizador"}
        for row, name in rows.items():
            line = next(l for l in output.splitlines() if l.startswith(name) and "/" in l)
            train, train_n, test, test_n = re.findall(r"\d+", line.replace("(u = 2)", ""))
            pattern = r"\| %s \| \**%s de %s\** \| \**%s de %s\** \|" % (
                re.escape(row), train, train_n, test, test_n)
            with self.subTest(row=row):
                self.assertRegex(text, pattern)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_examples_are_not_presented_as_real_runs(self):
        flat = " ".join(NOTES.read_text(encoding="utf-8").split())
        self.assertIn("ejemplos escritos para esta actividad, no salidas reales de un asistente", flat)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_policy_matches_the_syllabus(self):
        syllabus = (ROOT / "SYLLABUS.md").read_text(encoding="utf-8")
        self.assertIn("prohibidas en el curso, salvo en la actividad guiada de la semana 15", syllabus)
        flat = " ".join(NOTES.read_text(encoding="utf-8").replace("\n> ", " ").split())
        self.assertIn("están **prohibidas** en el curso, salvo en la actividad guiada", flat)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_no_urls(self):
        for text in [NOTES.read_text(encoding="utf-8")] + (
                [SLIDES.read_text(encoding="utf-8")] if SLIDES.exists() else []):
            self.assertNotRegex(text, r"https?://")


class SlidesAreTrue(unittest.TestCase):
    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_terminal_blocks_in_slides(self):
        for block in slide_blocks("terminal|salidalarga"):
            for command, expected in split_commands(block):
                actual = run_shell(command).splitlines()
                position = 0
                # Una diapositiva puede omitir líneas, pero no cambiarlas ni reordenarlas.
                for line in expected:
                    line = line.strip()
                    if not line:
                        continue
                    with self.subTest(command=command, line=line):
                        found = [i for i in range(position, len(actual)) if actual[i].strip() == line]
                        self.assertTrue(found, f"no aparece en la salida real: {line}")
                        if found:
                            position = found[0] + 1

    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_code_blocks_in_slides_exist(self):
        known = known_code_lines()
        for block in slide_blocks("codigo|codigochico|codigomini"):
            for line in block:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)


if __name__ == "__main__":
    unittest.main()
