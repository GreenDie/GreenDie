"""Minimal PDF generator - no external libraries needed."""

import textwrap

# ------------------------------------------------------------------
# Low-level PDF helpers
# ------------------------------------------------------------------

class PDFWriter:
    def __init__(self):
        self.objects = []   # list of bytes, index 0 = obj 1
        self.buf = b""

    def add_obj(self, content: bytes) -> int:
        """Append an indirect object; return its 1-based number."""
        self.objects.append(content)
        return len(self.objects)

    # ---- content streams ----------------------------------------

    def _encode_str(self, s: str) -> str:
        """Escape special chars for PDF string literals."""
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def build(self, page_streams: list[bytes], page_w=595, page_h=842) -> bytes:
        """Build final PDF bytes from a list of page content streams."""
        out = b"%PDF-1.4\n"
        offsets = []
        obj_num = 0

        def next_obj(body: bytes) -> int:
            nonlocal obj_num, out
            obj_num += 1
            offsets.append(len(out))
            out += f"{obj_num} 0 obj\n".encode()
            out += body
            out += b"\nendobj\n"
            return obj_num

        # Catalogue + Pages placeholder (will be filled after we know page ids)
        # We'll use a two-pass approach: collect all objects first, then write.

        objects = []  # list of raw dict/stream bodies as bytes

        n_pages = len(page_streams)

        # Reserve object slots:
        # 1 = catalog, 2 = pages, 3..2+n = page objects, then streams
        # Easier: just build everything and track numbers.

        out = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        obj_bodies = {}   # obj_number -> bytes (complete obj body incl dict)
        offsets_map = {}  # obj_number -> byte offset
        counter = [0]

        def alloc():
            counter[0] += 1
            return counter[0]

        cat_id    = alloc()  # 1
        pages_id  = alloc()  # 2
        font_id   = alloc()  # 3

        page_ids    = [alloc() for _ in page_streams]   # 4..
        content_ids = [alloc() for _ in page_streams]   # 4+n..

        # Font object
        obj_bodies[font_id] = (
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>"
        )
        obj_bodies[font_id + 0]  # just reference it

        # Font (mono) for formulas
        font_mono_id = alloc()
        obj_bodies[font_mono_id] = (
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier "
            b"/Encoding /WinAnsiEncoding >>"
        )

        # Content streams
        for i, stream in enumerate(page_streams):
            body = (
                f"<< /Length {len(stream)} >>\nstream\n".encode()
                + stream
                + b"\nendstream"
            )
            obj_bodies[content_ids[i]] = body

        # Page objects
        for i, pid in enumerate(page_ids):
            obj_bodies[pid] = (
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {page_w} {page_h}] "
                f"/Contents {content_ids[i]} 0 R "
                f"/Resources << /Font << /F1 {font_id} 0 R /F2 {font_mono_id} 0 R >> >> >>"
            ).encode()

        # Pages dict
        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        obj_bodies[pages_id] = (
            f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} >>"
        ).encode()

        # Catalog
        obj_bodies[cat_id] = (
            f"<< /Type /Catalog /Pages {pages_id} 0 R >>"
        ).encode()

        # Write all objects in numeric order
        out = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        for oid in sorted(obj_bodies.keys()):
            offsets_map[oid] = len(out)
            out += f"{oid} 0 obj\n".encode()
            out += obj_bodies[oid]
            out += b"\nendobj\n"

        # xref
        xref_pos = len(out)
        total = counter[0]
        out += f"xref\n0 {total+1}\n".encode()
        out += b"0000000000 65535 f \n"
        for oid in range(1, total + 1):
            out += f"{offsets_map[oid]:010d} 00000 n \n".encode()

        out += (
            f"trailer\n<< /Size {total+1} /Root {cat_id} 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode()

        return out


# ------------------------------------------------------------------
# High-level page builder
# ------------------------------------------------------------------

class Page:
    """Builds a PDF content stream for one page (A4, pt units)."""

    W, H = 595, 842
    MARGIN = 50
    LINE_H = 14

    def __init__(self):
        self.ops = []
        self.y = self.H - self.MARGIN  # current y (from bottom)

    def _escape(self, text: str) -> str:
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def _text(self, x, y, text, font="F1", size=11):
        self.ops.append(
            f"BT /{font} {size} Tf {x} {y} Td ({self._escape(text)}) Tj ET"
        )

    def _rect_fill(self, x, y, w, h, r, g, b):
        self.ops.append(
            f"{r:.3f} {g:.3f} {b:.3f} rg {x} {y} {w} {h} re f"
        )

    def _reset_color(self):
        self.ops.append("0 0 0 rg")

    # ---- public helpers ------------------------------------------

    def heading(self, text: str, size=13):
        """Green filled rectangle with white text."""
        bh = size + 6
        self._rect_fill(self.MARGIN, self.y - bh + 4, self.W - 2*self.MARGIN, bh, 0.13, 0.54, 0.13)
        self.ops.append("1 1 1 rg")
        self._text(self.MARGIN + 4, self.y - size + 2, text, size=size)
        self._reset_color()
        self.y -= bh + 4

    def section(self, title: str):
        """Light-green filled section header."""
        bh = 11 + 4
        self._rect_fill(self.MARGIN, self.y - bh + 3, self.W - 2*self.MARGIN, bh, 0.86, 0.94, 0.86)
        self.ops.append("0 0.31 0 rg")
        self._text(self.MARGIN + 3, self.y - 11 + 1, title, "F1", 11)
        self._reset_color()
        self.y -= bh + 4

    def text(self, line: str, size=10, indent=0):
        """Normal body text (wraps long lines)."""
        max_chars = 88 - indent * 3
        for wrapped in textwrap.wrap(line, max_chars) if line else [""]:
            self._text(self.MARGIN + indent * 10, self.y - size, wrapped, "F1", size)
            self.y -= self.LINE_H
        if not line:
            self.y -= 4

    def formula(self, line: str):
        """Light-grey Courier box."""
        bh = 11 + 4
        self._rect_fill(self.MARGIN, self.y - bh + 3, self.W - 2*self.MARGIN, bh, 0.95, 0.95, 0.95)
        self._text(self.MARGIN + 6, self.y - 11 + 1, line, "F2", 10)
        self.y -= bh + 2

    def space(self, pts=6):
        self.y -= pts

    def stream(self) -> bytes:
        return "\n".join(self.ops).encode("latin-1")

    def remaining(self):
        return self.y - self.MARGIN


# ------------------------------------------------------------------
# Content
# ------------------------------------------------------------------

def build_pages():
    pages = []

    # === PAGE 1 ===
    p = Page()
    p.heading("Drehstrom (3-Phasen-Wechselstrom) - Zusammenfassung", size=13)
    p.space(8)

    p.section("Grundbegriffe")
    p.text("Leistungsarten in Drehstromnetzen:", indent=1)
    p.formula("Wirkleistung   P  [W]    - wird in Waerme/Arbeit umgewandelt")
    p.formula("Blindleistung  Q  [var]  - wird gespeichert und zurueckgegeben")
    p.formula("Scheinleistung S  [VA]   - S = sqrt(P^2 + Q^2)")
    p.text("Leistungsfaktor: cos(phi) = P / S   (phi = Winkel im Leistungsdreieck)", indent=1)
    p.formula("Parallelwiderstand: R_Ers = (R1 * R2) / (R1 + R2)")
    p.space(8)

    p.section("Aufgabe 1 - Sternschaltung (Grundformel)")
    p.text("Gegeben: U_L = 400 V (Leiterspannung)", indent=1)
    p.formula("U_str = U_L / sqrt(3) = 400 V / 1,732 = 230,94 V")
    p.text("Die Strangspannung (~230 V) entspricht der bekannten Haushaltsspannung.", indent=1)
    p.space(8)

    p.section("Aufgabe 2 - Sternschaltung, rein ohmsche Last  (phi = 0 deg, R = 32 Ohm)")
    p.text("a) Strangspannung:", indent=1)
    p.formula("U_str = U_L / sqrt(3) = 230,94 V")
    p.text("b) Strangstrom:", indent=1)
    p.formula("I_str = U_str / R = 230,94 V / 32 Ohm = 7,21 A")
    p.text("c) Strangleistung:", indent=1)
    p.formula("P_str = U_str * I_str = 230,94 V * 7,21 A = 1 665,07 W")
    p.text("d) Gesamtleistung (zwei Berechnungswege):", indent=1)
    p.formula("P_ges = 3 * P_str = 3 * 1 665,07 W = 4 995,21 W")
    p.formula("P_ges = sqrt(3) * U_L * I_L * cos(phi)")
    p.formula("      = 1,732 * 400 V * 7,21 A * 1 = 4 995,23 W   (Probe: OK)")
    p.space(8)

    p.section("Aufgabe 3 - Dreieckschaltung  (P_ges = 9 kW, U_L = 400 V)")
    p.text("a) Strangleistung:", indent=1)
    p.formula("P_str = P_ges / 3 = 9 000 W / 3 = 3 000 W = 3 kW")
    p.text("b) Strangwiderstand:", indent=1)
    p.formula("I_str = P_str / U_str = 3 000 W / 400 V = 7,5 A")
    p.formula("R_str = U_str / I_str = 400 V / 7,5 A = 53,3 Ohm")
    p.text("c) & d) Anteiliger lambda-Anteil der Strangleistung:", indent=1)
    p.formula("P_lambda     = 1/3 * P_ges     = 3 kW")
    p.formula("P_str,lambda = 1/3 * P_lambda  = 1 kW")
    p.space(10)

    p.section("Kernaussage")
    p.text(
        "Der Tafelinhalt behandelt die Berechnung von Spannungen, Stroemen und Leistungen "
        "in symmetrischen Drehstromnetzen - sowohl fuer Stern- als auch Dreieckschaltungen. "
        "Dabei wird zwischen Strang- und Leiterspannung/-strom unterschieden und die "
        "Gesamtleistung auf zwei Wegen ermittelt (Formel direkt + Drehstromformel).",
        indent=1
    )

    pages.append(p.stream())
    return pages


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

if __name__ == "__main__":
    writer = PDFWriter()
    page_streams = build_pages()
    pdf_bytes = writer.build(page_streams)

    out_path = "/home/user/GreenDie/Drehstrom_Zusammenfassung.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"PDF erstellt: {out_path}  ({len(pdf_bytes):,} Bytes)")
