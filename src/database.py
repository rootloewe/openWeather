import sqlite3
import logging


logger = logging.getLogger(__name__)


class DataBase:
    """
    Initialisiert die Datenbankverbindung SQLite und erstellt die Tabelle "wetter".

    Diese Methode stellt eine Verbindung zur SQLite-Datenbankdatei "wetterdaten.db" her.
    Falls die Tabelle "wetter" noch nicht existiert, wird sie mit den Spalten ID, Ort, Temperature,
    Description_DE und Description_EN angelegt.

    Die Tabelle wird so erstellt, dass doppelte Einträge für ID vermieden werden (Primärschlüssel).

    Nach der Erstellung der Tabelle wird die Verbindung zur Datenbank gespeichert.

    Beispiel:
    >>> db = DataBase()
    >>> # Datenbank und Tabelle wurden initialisiert

    Returns:
        None
    """
    def __init__(self):
        sql = """
            CREATE TABLE IF NOT EXISTS wetter (
                ID INTEGER PRIMARY KEY,
                Ort TEXT,
                Temperature REAL,
                Description_DE TEXT,
                Description_EN TEXT
            );
        """
        try:
            self.conn = sqlite3.connect("../db/wetterdaten.db") 
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"SQLite Fehler: {e}")
        except Exception as e:
            logger.error(f"Unerwarteter Fehler aufgetreten: {e}")
        else:
            cursor.close()
     

    def fill_db(self, results: list) -> None:
        """
        Fügt mehrere Wetterdatensätze aus einer Ergebnisliste in die Datenbanktabelle "wetter" ein.

        Diese Methode extrahiert aus der übergebenen Liste `results` die Namen (Orte),
        Temperaturwerte und Wetterbeschreibungen (Deutsch und Englisch) und fügt diese
        als neue Einträge in die Tabelle "wetter" ein.

        Args:
            results (list): Eine Liste von Dictionaires mit Wetterdaten, 
                            wobei jedes Element mindestens die Schlüssel
                            'name', 'main' und 'weather' enthält.

        Beispiel:
            >>> results = [
            >>>     {'name': 'Berlin', 'main': {'temp': 10.4}, 'weather': [{'description': 'Bedeckt'}, {'description': 'overcast clouds'}]},
            >>>     {'name': 'Aachen', 'main': {'temp': 8.9}, 'weather': [{'description': 'Klarer Himmel'}, {'description': 'clear sky'}]}
            >>> ]
            >>> db.fill_db(results)

        Hinweis:
            - Es wird `executemany` verwendet, um mehrere Datensätze effizient einzufügen.
            - Nach dem Einfügen erfolgt ein Commit, um die Änderungen dauerhaft zu speichern.
            - Der Cursor wird nach der Nutzung geschlossen.

        Returns:
            None
        """
        namen = [eintrag['name'] for eintrag in results]
        temp = [eintrag['main']['temp'] for eintrag in results]
        desc = [eintrag['weather'][0]['description'] for eintrag in results]
            
        params = (
            (namen[0], temp[0], desc[0], desc[1]),
            (namen[2], temp[2], desc[2], desc[3]),
            (namen[4], temp[4], desc[4], desc[5])
        )

        sql = """INSERT INTO wetter (Ort, Temperature, Description_DE, Description_EN) VALUES (?,?,?,?)"""
        cursor = self.conn.cursor()
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            logger.exception(f"Fehler beim Einfügen in die Datenbank: {e}")
        except Exception as e:
            logger.error(f"Unbekannter Fehler aufgetreten: {e}")
        else:
            cursor.close()
         


    def read_db(self) -> None:
        """
        Liest alle Einträge aus der Tabelle "wetter" aus und gibt sie auf der Konsole aus.

        Diese Methode führt eine SQL SELECT-Anweisung aus, um alle Datensätze aus der Tabelle "wetter" abzurufen.
        Die Ergebnisse werden zeilenweise iteriert und für jeden Datensatz werden Ort, Temperatur,
        sowie deutsche und englische Wetterbeschreibung ausgegeben.

        Nach Abschluss der Abfrage wird der Datenbank-Cursor geschlossen.

        Beispiel:
            >>> db.read_db()
            Berlin 10.42 Bedeckt overcast clouds
            Aachen 8.89 Klarer Himmel clear sky

        Returns:
            None
        """
        cursor = self.conn.cursor()
        sql = """SELECT * FROM wetter"""
        try:
            cursor.execute(sql)
        except Exception as e:
            logger.error(f"Fehler beim Schließen des Cursors: {e}")
        else:
            ausgabe = cursor.fetchall()

            print(f"\n{'Ort':^7}{'Temp':^26}{'Deutsch':^12}{'Englisch':^39}")
            print("-" * 73) 
            for _, ort, temp, de, en in ausgabe:
                temp_str = f"{temp:.2f} °C"
                print(f"{ort:<16}{temp_str:<15}{de:<27}{en:<20}")
            print()

            cursor.close()


    def disconnect_db(self) -> None:
        """
        Schließt die Verbindung zur SQLite-Datenbank.

        Diese Methode prüft, ob die Datenbankverbindung noch offen ist, und schließt sie dann.
        Das Schließen der Verbindung gibt Ressourcen frei und verhindert mögliche
        Datenbank-Locks oder Speicherlecks.

        Es sollte sichergestellt sein, dass nach Aufruf dieser Methode keine weiteren
        Operationen auf der Datenbankverbindung durchgeführt werden.

        Beispiel:
            >>> db.disconnect_db()
            # Datenbankverbindung wird geschlossen

        Returns:
            None
        """
        try:
            self.conn.close()
        except Exception as e:
            logger.error(f"Fehler beim Schließen der Verbindung: {e}")
     

