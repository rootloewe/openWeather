__author__ = "Armin"
__version__ = "1.5.2"
__doc__ = """
Dieses Programm holt sich Wetterdaten von openWeather.com und Schreibt für drei Beispielstädte einige
ausgewählte Daten in eine SQLite.
"""
from weather_api import WeatherAPI
from database import DataBase
import logging
import config as cfg


logger = logging.getLogger()


def main():
    """
    Hauptfunktion, die den gesamten Ablauf steuert: Datenbankverbindung aufbauen,
    API-Daten abrufen, in die Datenbank schreiben, auslesen und schließen.

    Ablauf:
        - Instanziiert eine Datenbankverbindung.
        - Lädt den API-Schlüssel mittels `get_api_key`.
        - Erzeugt ein WeatherAPI-Objekt mit dem API-Schlüssel.
        - Holt aktuelle Wetterdaten von der API.
        - Speichert die Wetterdaten in der Datenbank.
        - Liest die Daten aus der Datenbank und gibt sie aus.
        - Schließt die Datenbankverbindung.

    Returns:
        None

    Beispiel:
        >>> main()
    """
    conn = None
    API_KEY = cfg.API_KEY
    weather_api = WeatherAPI(API_KEY)

    conn = DataBase()
    raw_data_list = weather_api.get_weather_data()
    conn.fill_db(raw_data_list)
    conn.read_db()
    
    if conn is not None:
        conn.disconnect_db()


if __name__ == "__main__":
    logger.info(f"Anwendung {cfg.APP_TITLE} Version {cfg.APP_VERSION} gestartet.")
    main()
    logger.info(f"Anwendung {cfg.APP_TITLE} Version {cfg.APP_VERSION} beendet.")

