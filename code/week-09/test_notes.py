"""Vuelve a correr los comandos que aparecen en los apuntes y en las diapositivas
y comprueba que el código citado existe de verdad en esta carpeta.

Casi toda la salida de este capítulo depende de la máquina, así que un comentario antes
del bloque dice cómo se compara:
  <!-- direcciones -->  igual, salvo las direcciones
  <!-- sanitizer -->    solo las frases estables del informe
  <!-- esta corrida --> comportamiento indefinido o datos del sistema: no se compara
En las diapositivas, los entornos salidadir, salidasan y salidacorrida dicen lo mismo.
"""
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
NOTES = ROOT / "notes" / "week-09.md"
SLIDES = ROOT / "slides" / "week-09.tex"
STABLE = [
    r"stack-buffer-overflow",
    r"READ of size 4",
    r"WRITE of size 4",
    r"runtime error: index \d+ out of bounds for type 'int \[\d+\]'",
    r"errors/\w+\.c:\d+",
]
MARKS = {"<!-- direcciones -->": "addresses", "<!-- sanitizer -->": "sanitizer",
         "<!-- esta corrida -->": "run"}


def normalize(text):
    # Según el idioma del entorno, gcc usa comillas tipográficas o rectas.
    return text.replace("‘", "'").replace("’", "'")


def hide_addresses(text):
    return re.sub(r"0x[0-9a-f]+", "0x...", text)


def run_shell(command):
    done = subprocess.run(
        ["bash", "-c", command], cwd=HERE, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
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
    """Devuelve (líneas, tipo de comparación) de cada bloque de los apuntes."""
    blocks, current, mark, previous = [], None, None, ""
    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^> ?", "", raw)
        if current is None:
            if line.strip() == "```" + language:
                current, mark = [], MARKS.get(previous.strip())
            elif line.strip():
                previous = line
        elif line.strip() == "```":
            blocks.append((current, mark))
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


def stable_phrases(line):
    return [m.group(0) for pattern in STABLE for m in re.finditer(pattern, line)]


class Case(unittest.TestCase):
    def check_sanitizer_block(self, block):
        for command, expected in split_commands(block):
            actual = run_shell(command)
            for line in expected:
                for phrase in stable_phrases(line):
                    with self.subTest(command=command, phrase=phrase):
                        self.assertIn(phrase, actual)

    def check_addresses_subset(self, block):
        """Una diapositiva puede omitir líneas, pero no cambiarlas ni reordenarlas."""
        for command, expected in split_commands(block):
            actual = hide_addresses(run_shell(command)).splitlines()
            position = 0
            for line in expected:
                line = hide_addresses(line).strip()
                if not line or line == "...":
                    continue
                with self.subTest(command=command, line=line):
                    found = [i for i in range(position, len(actual)) if actual[i].strip() == line]
                    self.assertTrue(found, f"no aparece en la salida real: {line}")
                    if found:
                        position = found[0] + 1


class NotesAreTrue(Case):
    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_terminal_blocks_in_notes(self):
        checked = 0
        for lines, mark in note_blocks("text"):
            if not lines or not lines[0].startswith("$ "):
                continue
            if mark == "sanitizer":
                self.check_sanitizer_block(lines)
                continue
            for command, expected in split_commands(lines):
                actual = run_shell(command).rstrip("\n")
                checked += 1
                with self.subTest(command=command):
                    if mark == "addresses":
                        self.assertEqual(hide_addresses(actual), hide_addresses("\n".join(expected)))
                    elif mark is None:
                        self.assertEqual(actual, "\n".join(expected))
        self.assertGreater(checked, 10)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_code_blocks_in_notes_exist(self):
        known = known_code_lines()
        for lines, _ in note_blocks("c"):
            for line in lines:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_hierarchy_numbers_are_labeled_as_approximate(self):
        text = NOTES.read_text(encoding="utf-8")
        self.assertIn("órdenes de magnitud aproximados", text)
        self.assertIn("Tiempo de un acceso (aproximado)", text)


class SlidesAreTrue(Case):
    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_terminal_blocks_in_slides(self):
        for block in slide_blocks("terminal|salidalarga|salidadir"):
            self.check_addresses_subset(block)

    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_sanitizer_blocks_in_slides(self):
        for block in slide_blocks("salidasan"):
            self.check_sanitizer_block(block)

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
