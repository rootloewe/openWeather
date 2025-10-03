# OpenWeatherMap Wetter App in Python

Dieses Projekt ist eine Python-Anwendung, die Wetterdaten von der OpenWeatherMap API abruft und anzeigt. Am Beispiel von drei Städten und die Daten in eine SQLite Datenbank schreibt. Es wurde auch ein Logging bereitgestellt in Datei und in Konsole.

## Voraussetzungen

- Python 3.x
- Ein OpenWeatherMap API-Schlüssel (kostenlos auf https://openweathermap.org/ erhältlich)
- Die Python-Bibliothek `requests`
- `python-dotenv`, um Umgebungsvariablen aus der `semple.env` Datei zu laden, eigenen Schlüssel eintragen

## Installation

1. Klonen Sie das Repository oder laden Sie die Dateien herunter.
2. pip install sqlite pandas dotenv requests siehe requirements.txt
3. Erstellen Sie eine virtuelle Umgebung (optional):

## Konsolenausgabe
root - 2025-10-02 03:43:03 - app.py - 70 - INFO - Anwendung gestartet

|   Ort     |   Temp  |      Deutsch      |     Englisch     |
|-----------|---------|-------------------|------------------|
| Berlin    | 8.25 °C | Bedeckt           | overcast clouds  |
| München   | 6.20 °C | Ein paar Wolken   | few clouds       |
| Stuttgart | 3.87 °C | Klarer Himmel     | clear sky        |

root - 2025-10-02 03:43:04 - app.py - 72 - INFO - Anwendung beendet

## Lizenz
GNU GENERAL PUBLIC LICENSE
