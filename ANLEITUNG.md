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

Jedes Feld lässt sich von Hand tippen oder mit **Jetzt** auf die aktuelle Uhrzeit stempeln.
Gestempelt wird immer auf die nächsten vollen 5 Minuten aufgerundet: um 6:27 gedrückt
ergibt 6:30, um 12:31 gedrückt ergibt 12:35. Von Hand eingetippte Zeiten bleiben
unverändert stehen.
Der Knopf **Pause starten** setzt den Pausenbeginn, beim zweiten Druck (**Pause beenden**)
das Pausenende.

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
| Auftrag / Tätigkeit | mehrzeilig — was gemacht wurde |
| Material | mehrzeilig — verbaute Teile, Mengen |
| Beginn / Ende | Uhrzeiten, von Hand oder per Stoppuhr |

- **+ Auftrag** legt einen neuen Auftrag an.
- **Start** / **Stopp** stempeln Beginn und Ende, ebenfalls auf 5 Minuten aufgerundet.
  Während der Messung läuft die Uhr rechts sekundengenau mit; beim Stopp zählt die
  Zeit zwischen den beiden gestempelten Zeiten.
- Solange etwas läuft, zeigt das Band ganz oben Kunde und laufende Zeit — auch wenn du
  gerade einen anderen Tag ansiehst. Der Stopp-Knopf dort beendet die Messung von überall.
- Es läuft immer nur ein Auftrag: startest du einen zweiten, wird der erste automatisch gestoppt.
- Der allererste Start am Tag stempelt den Arbeitsbeginn mit, falls er noch leer ist.
- Zeiten lassen sich jederzeit von Hand nachbessern — dann zählt die eingetippte Zeit.

## Tage, Monat, Export

Mit **‹** und **›** blätterst du durch die Tage, **Heute** springt zurück.
Die **Monatsübersicht** listet alle erfassten Tage des angezeigten Monats mit Summe unten.

Die **Auftragsübersicht** zeigt denselben Monat aus Sicht der Aufträge:
oben die Summe je Kunde (nach Stunden sortiert, für die Abrechnung), darunter jeden
Einsatz einzeln mit Tätigkeit und Material. Ein Klick auf eine Zeile springt zu dem Tag.

- **CSV: Tage (Monat)** — Stundenzettel je Tag, mit Dezimalstunden und Monatssumme
- **CSV: Aufträge (Monat)** — jede Auftragszeit einzeln mit Kunde, Geburtsdatum,
  Tätigkeit und Material, für die Abrechnung
- **Sicherung speichern / laden** — alle Daten als JSON-Datei

Die CSV-Dateien sind mit Semikolon getrennt und haben Komma als Dezimaltrennzeichen,
lassen sich also in Excel per Doppelklick öffnen.

## Wichtig

Die Daten liegen im Speicher des Browsers. Löschst du die Browserdaten oder
deinstallierst den Browser, sind die Zeiten weg — deshalb ab und zu
**Sicherung speichern** drücken und die Datei ablegen.
