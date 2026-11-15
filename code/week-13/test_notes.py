"""Vuelve a correr los comandos que aparecen en los apuntes y en las diapositivas
y comprueba que el código citado existe de verdad en esta carpeta."""
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
NOTES = ROOT / "notes" / "week-13.md"
SLIDES = ROOT / "slides" / "week-13.tex"
# Antes de un bloque con direcciones o con comportamiento indefinido. De él solo se
# exigen estas cadenas estables, si el bloque las muestra.
MACHINE_DEPENDENT = "<!-- depende de la corrida -->"
STABLE = ["runtime error: signed integer overflow"]
# Antes de un bloque con tiempos. No se corre aquí, porque tarda y cambia en cada corrida:
# de él se revisan solo las cuentas, que son exactas.
MEASURED = "<!-- medición -->"
# En esta salida, solo las direcciones cambian.
ADDRESSES = re.compile(r"0x[0-9a-f]+")


def normalize(text):
    # Según el idioma del entorno, gcc usa comillas tipográficas o rectas.
    return ADDRESSES.sub("0x", text.replace("‘", "'").replace("’", "'"))


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


def note_blocks(language, marker=MACHINE_DEPENDENT):
    """Devuelve (líneas, tiene_la_marca) de cada bloque de los apuntes."""
    blocks, current, flagged, previous = [], None, False, ""
    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^> ?", "", raw)
        if current is None:
            if line.strip() == "```" + language:
                current, flagged = [], previous.strip() == marker
            elif line.strip():
                previous = line
        elif line.strip() == "```":
            blocks.append((current, flagged))
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
        measured = [lines for lines, marked in note_blocks("text", MEASURED) if marked]
        for lines, flagged in note_blocks("text"):
            if not lines or not lines[0].startswith("$ ") or lines in measured:
                continue
            for command, expected in split_commands(lines):
                actual = run_shell(command).rstrip("\n")
                checked += 1
                with self.subTest(command=command):
                    if flagged:
                        for token in STABLE:
                            if any(token in line for line in expected):
                                self.assertIn(token, actual)
                    else:
                        lines = [line.rstrip() for line in actual.split("\n")]
                        self.assertEqual("\n".join(lines), "\n".join(expected))
        self.assertGreater(checked, 20)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_code_blocks_in_notes_exist(self):
        known = known_code_lines()
        for lines, _ in note_blocks("c"):
            for line in lines:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_measured_blocks_have_exact_counts(self):
        rows = {"sort_times": 0, "sort_then_search": 0}
        measured = [lines for lines, marked in note_blocks("text", MEASURED) if marked]
        self.assertEqual(len(measured), 3)
        for block in measured:
            for command, output in split_commands(block):
                for line in output:
                    fields = line.split()
                    if "sort_times" in command and len(fields) == 5 and fields[0].isdigit():
                        n = int(fields[0])
                        self.assertEqual(int(fields[1]), n * (n - 1) // 2, line)
                        self.assertEqual(fields[4], "sí", line)
                        rows["sort_times"] += 1
                    if "sort_then_search" in command and len(fields) == 5 and fields[0].isdigit():
                        self.assertEqual(int(fields[1]), int(fields[0]) * 100000, line)
                        rows["sort_then_search"] += 1
        self.assertEqual(rows, {"sort_times": 7, "sort_then_search": 6})

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_notes_flag_what_depends_on_the_machine(self):
        text = " ".join(NOTES.read_text(encoding="utf-8").split())
        self.assertIn("en esta corrida", text)
        self.assertIn("esta máquina", text)
        self.assertEqual(text.count(MEASURED), 3)
        self.assertNotIn("TODO", text)


class SlidesAreTrue(unittest.TestCase):
    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_terminal_blocks_in_slides(self):
        for block in slide_blocks("terminal|terminalmini|salidalarga"):
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
    def test_measurements_in_slides_come_from_the_notes(self):
        notes = NOTES.read_text(encoding="utf-8")
        blocks = slide_blocks("informe")
        self.assertGreater(len(blocks), 0)
        for block in blocks:
            for line in block:
                if line.strip():
                    with self.subTest(line=line):
                        self.assertIn(line.rstrip(), notes)

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
