# Zeiterfassung

Eine einzelne Datei (`index.html`), die im Browser läuft — am Rechner wie am Handy.
Kein Konto, kein Internet nötig, keine Installation. Alle Zeiten bleiben auf deinem Gerät.

## Auf dem Handy einrichten

1. `index.html` auf das Gerät laden und im Browser öffnen.
2. Im Browsermenü **„Zum Startbildschirm hinzufügen"** wählen.
3. Danach startet die Zeiterfassung wie eine normale App — auch ohne Empfang.

Alternativ in den Repository-Einstellungen unter *Settings → Pages* die GitHub Pages
einschalten (Branch auswählen, Ordner `/root`). Dann ist die App unter
`https://greendie.github.io/GreenDie/` erreichbar.

## Der Arbeitstag

| Feld | Bedeutung |
|---|---|
| Arbeitsbeginn | Kommen, z. B. 06:30 |
| Pause von / bis | z. B. 12:30 bis 13:00 — beliebig viele Pausen über **+ Pause** |
| Arbeitsende | Gehen, z. B. 17:30 |

Zeiten werden direkt im Uhrfeld gewählt oder getippt. Jede bestätigte Uhrzeit wird auf
die nächsten vollen 5 Minuten aufgerundet: aus 6:27 wird 6:30, aus 12:31 wird 12:35.
Das gilt in allen Uhrfeldern der App.

Oben stehen laufend die Summen:

- **Anwesend** — Arbeitsende minus Arbeitsbeginn
- **Pause** — alle Pausen zusammen
- **Arbeitszeit** — Anwesenheit minus Pausen, zusätzlich als Dezimalstunden (10:30 = 10,50 h)
- **Auf Aufträge** — wie viel davon schon auf Aufträge gebucht ist und wie viel noch offen

Schichten über Mitternacht (22:00 bis 02:30) werden korrekt gerechnet.

## Aufträge

Pro Auftrag werden erfasst:

| Feld | |
|---|---|
| Kunde | Name |
| Geburtsdatum | z. B. 04.09.1958 |
| Abfahrt | Uhrzeit, wann du losgefahren bist |
| Ankunft | Uhrzeit beim Kunden |
| Anfahrt | Fahrzeit in Minuten, z. B. 20 |
| Tätigkeiten | Liste — jede Zeile mit eigener Uhrzeit, **+ Tätigkeit** hängt eine an |
| Material | Liste — eine Zeile je Teil, **+ Material** hängt eine an |
| Heimfahrt | Uhrzeit, wann du beim Kunden losgefahren bist |
| Dauer | wird gerechnet: Ankunft bis Heimfahrt |

Tätigkeiten und Material sind Listen statt Textfelder: jede Zeile ist ein eigener
Eintrag, das × daneben löscht sie.

Die Uhrzeit einer neuen Tätigkeit ist mit **einer Stunde Vorlauf** vorbelegt: legst du
um 9:07 eine an, steht dort 10:10. Mit **−15** und **+15** links und rechts vom Uhrfeld
schiebst du sie in Viertelstundenschritten zurecht, ohne den Zeitwähler zu öffnen.

**Enter** im Textfeld hängt gleich die nächste Zeile an und springt hinein — so lässt
sich eine Liste durchtippen, ohne zwischendurch einen Knopf zu treffen. Ist das Feld
noch leer, passiert nichts, damit keine Leerzeilen entstehen.

**+ Auftrag** legt einen neuen Auftrag an, das × in der Kopfzeile der Karte löscht ihn
nach Rückfrage. Die Dauer unten rechts rechnet sich laufend aus Ankunft und Heimfahrt
und fließt in die Summe **Auf Aufträge** oben ein.

## Tage, Monat, Export

Mit **‹** und **›** blätterst du durch die Tage, **Heute** springt zurück.
Die **Monatsübersicht** listet alle erfassten Tage des angezeigten Monats mit Summe unten.

Die **Auftragsübersicht** listet die Aufträge des Monats mit Kunde, Ankunft, Anfahrt
und allen Tätigkeiten samt Uhrzeiten; unten steht die gesamte Anfahrtszeit.
Ein Klick auf eine Zeile springt zu dem Tag. Auf dem Handy wird daraus je Auftrag
eine Karte, damit nichts seitlich aus dem Bild läuft.

- **CSV: Tage (Monat)** — Stundenzettel je Tag, mit Dezimalstunden und Monatssumme
- **CSV: Aufträge (Monat)** — jeder Auftrag einzeln mit Kunde, Geburtsdatum, Abfahrt,
  Ankunft, Anfahrt, Tätigkeiten, Material, Heimfahrt und Dauer
- **Sicherung speichern / laden** — alle Daten als JSON-Datei

Die CSV-Dateien sind mit Semikolon getrennt und haben Komma als Dezimaltrennzeichen,
lassen sich also in Excel per Doppelklick öffnen.

## Wichtig

Die Daten liegen im Speicher des Browsers. Löschst du die Browserdaten oder
deinstallierst den Browser, sind die Zeiten weg — deshalb ab und zu
**Sicherung speichern** drücken und die Datei ablegen.
