import logging
import logging.config
from dotenv import load_dotenv
import os
from pathlib import Path
import json

os.chdir(str(Path(__file__).parent.resolve()))

config_path = Path("../configs") / "config.json"
logging_pfad = Path("../configs") / "logging.ini"

logging.config.fileConfig(logging_pfad)


def get_api_key() -> str:
    """
    Lädt den API-Schlüssel aus einer Umgebungsvariablen-Datei und gibt ihn zurück.

    Die Funktion lädt Umgebungsvariablen aus der Datei 'config/sample.env' und liest den Wert
    der Variablen "API_KEY" aus. Dieser Schlüssel wird zur Authentifizierung bei externen APIs verwendet.

    Returns:
        str: Der API-Schlüssel, wenn vorhanden, sonst None.

    Beispiel:
        >>> api_key = get_api_key()
        >>> print(api_key)
        your_api_key_value
    """
    api_key = None
    env_path = Path('../configs/sample.env')

    try:
        load_dotenv(dotenv_path=env_path)  
        api_key = os.getenv("API_KEY")

    except FileNotFoundError as fnf_error:
        logging.error(f".env Datei nicht gefunden: {fnf_error}")
    
    except ValueError as val_error:
        logging.error(f"Fehler bei API_KEY: {val_error}")
       
    except Exception as e:
        logging.error(f"Unerwarteter Fehler: {e}")
    
    finally:
        return api_key


try:
    file = open(config_path, mode = "r", encoding= "UTF-8")
    config = json.load(file)

except FileNotFoundError as fnf_error:
    logging.error(f"config Datei nicht gefunden: {fnf_error}")
except IOError as e:
    logging.error(f"Ein I/O Fehler ist aufgetreten: {e}")
else:
    file.close()


API_KEY = get_api_key()

APP_TITLE = config["app"]["app_title"]
APP_VERSION = config["app"]["app_version"]