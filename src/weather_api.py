import requests
import logging


logger = logging.getLogger(__name__)

"""
Interface zur OpenWeatherMap API, um Wetterdaten für vordefinierte Städte in mehreren Sprachen abzurufen.

Eigenschaften
----------
BASE_URL : str
    Die Basis-URL für die OpenWeatherMap API.
api_key : str
    API-Schlüssel für den Zugriff auf die Wetterdaten.
CITIES : list of str
    Liste der Städte, für die Wetterdaten abgefragt werden.
LANGS : list of str
    Liste der Sprachcodes, in denen die Wetterbeschreibung angefordert wird.
units : str
    Einheitensystem für Temperaturwerte (z.B. "metric" für Celsius).

Methoden
-------
build_url():
    Erstellt die vollständigen API-Abfrage-URLs für alle Städte und Sprachen.
get_weather_data():
    Ruft die Wetterdaten von der API ab und gibt die Ergebnisse als JSON zurück.
"""
class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key, units="metric"):
        """
        Initialisiert die WeatherAPI-Instanz mit API-Schlüssel, Städte- und Spracheinstellungen.

        Parameters
        ----------
        api_key : str
            Der API-Schlüssel zur Authentifizierung bei OpenWeatherMap.
        units : str, optional
            Einheitensystem für Temperaturwerte (Standard ist "metric").
        """
        self.api_key = api_key
        self.CITIES = ["Berlin", "München", "Stuttgart"]
        self.LANGS = ["DE", "EN"]
        self.units = units
        

    def build_url(self) -> list:
        """
        Erzeugt eine Liste von URL-Abfragen für alle angegebenen Städte und Sprachen.

        Returns
        -------
        list of str
            Eine Liste von API-URLs zur Abfrage der Wetterdaten.
        """
        urls = []
        for city in self.CITIES:
            for lang in self.LANGS:
                url = f"{self.BASE_URL}?q={city}&appid={self.api_key}&units={self.units}&lang={lang}"
                urls.append(url)
        return urls 


    def get_weather_data(self):
        """
        Ruft die aktuellen Wetterdaten von OpenWeatherMap für alle URLs ab.

        Returns
        -------
        list of dict
            Liste mit JSON-Daten der Wetterinformationen für jede Stadt und Sprache.
        
        Raises
        ------
        requests.HTTPError
            Wenn eine HTTP-Anfrage fehlschlägt.
        """
        urls = self.build_url()
        results = []
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                results.append(response.json())
            except requests.RequestException as e:
                logger.exception(f"Fehler beim Abruf der URL {url}: {e}")
                
        return results