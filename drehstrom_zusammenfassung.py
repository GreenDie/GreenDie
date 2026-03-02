from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(34, 139, 34)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "Drehstrom – Zusammenfassung", align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Seite {self.page_no()}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(220, 240, 220)
        self.set_text_color(0, 80, 0)
        self.cell(0, 9, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def formula_line(self, text):
        self.set_font("Courier", "", 11)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 7, "  " + text, fill=True)
        self.ln(1)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# --- Grundbegriffe ---
pdf.section_title("Grundbegriffe")
pdf.body_text("Leistungsarten in Drehstromnetzen:")
pdf.formula_line("Wirkleistung   P  [W]")
pdf.formula_line("Blindleistung  Q  [var]")
pdf.formula_line("Scheinleistung S  [VA]")
pdf.body_text("Leistungsdreieck mit Winkel phi (cos phi = Leistungsfaktor)")
pdf.formula_line("Parallelwiderstand: R_Ersatz = (R1 * R2) / (R1 + R2)")

# --- Aufgabe 1 ---
pdf.section_title("Aufgabe 1 – Sternschaltung (Grundformel)")
pdf.body_text("Gegebene Leiterspannung: U_L = 400 V")
pdf.formula_line("U_str = U_L / sqrt(3) = 400 V / 1,732 = 230,94 V")
pdf.body_text("Die Strangspannung betraegt ca. 230 V – das entspricht der bekannten Haushaltsspannung.")

# --- Aufgabe 2 ---
pdf.section_title("Aufgabe 2 – Sternschaltung, rein ohmsche Last (phi = 0°, R = 32 Ohm)")
pdf.body_text("a) Strangspannung:")
pdf.formula_line("U_str = U_L / sqrt(3) = 230,94 V")
pdf.body_text("b) Strangstrom:")
pdf.formula_line("I_str = U_str / R = 230,94 V / 32 Ohm = 7,21 A")
pdf.body_text("c) Strangleistung:")
pdf.formula_line("P_str = U_str * I_str = 230,94 V * 7,21 A = 1 665,07 W")
pdf.body_text("d) Gesamtleistung (zwei Wege):")
pdf.formula_line("P_ges = 3 * P_str = 3 * 1 665,07 W = 4 995,21 W")
pdf.formula_line("P_ges = sqrt(3) * U_L * I_L * cos(phi)")
pdf.formula_line("      = 1,732 * 400 V * 7,21 A * 1 = 4 995,23 W  (Probe: OK)")

# --- Aufgabe 3 ---
pdf.section_title("Aufgabe 3 – Dreieckschaltung (P_ges = 9 kW, U_L = 400 V)")
pdf.body_text("a) Strangleistung:")
pdf.formula_line("P_str = P_ges / 3 = 9 000 W / 3 = 3 000 W = 3 kW")
pdf.body_text("b) Strangwiderstand:")
pdf.formula_line("I_str = P_str / U_str = 3 000 W / 400 V = 7,5 A")
pdf.formula_line("R_str = U_str / I_str = 400 V / 7,5 A = 53,3 Ohm")
pdf.body_text("c) & d) Anteilige Strangleistung (lambda-Anteil):")
pdf.formula_line("P_lambda     = 1/3 * P_ges  = 3 kW")
pdf.formula_line("P_str,lambda = 1/3 * P_lambda = 1 kW")

# --- Kernaussage ---
pdf.section_title("Kernaussage")
pdf.body_text(
    "Der Tafelinhalt behandelt die Berechnung von Spannungen, Stroemen und Leistungen "
    "in symmetrischen Drehstromnetzen – sowohl fuer die Stern- als auch fuer die "
    "Dreieckschaltung. Dabei wird zwischen Strang- und Leiterspannung/-strom "
    "unterschieden und die Gesamtleistung auf zwei Wegen ermittelt (direkt und "
    "ueber die Drehstromformel)."
)

pdf.output("/home/user/GreenDie/Drehstrom_Zusammenfassung.pdf")
print("PDF erstellt!")
