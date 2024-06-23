# wsgi.py
import os
from api import API
from database import Database
from headless import HeadlessPlayer

def create_app():
    # Load configurations from environment variables
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", 5432))
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    api_host = os.getenv("API_HOST", "localhost")
    api_port = int(os.getenv("API_PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    force = os.getenv("FORCE", "false").lower() == "true"
    timeout = int(os.getenv("TIMEOUT", 5))
    without_api = os.getenv("NOAPI", "false").lower() == "true"

    # Initialize the database
    db = Database(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    db.test()
    if force:
        db.clear()
    db.init()

    if not without_api:
        print("[EDGESIGHT] Starting with API...")
        api = API(database=db, headless=HeadlessPlayer(again_after=timeout))
        return api.app
    else:
        print("[EDGESIGHT] Starting without API...")
        headless_player = HeadlessPlayer(database=db, again_after=timeout)
        headless_player.start()
        return None

# Create the WSGI application object
application = create_app()

if __name__ == "__main__":
    from waitress import serve
    serve(application, host="0.0.0.0", port=int(os.getenv("API_PORT", 5000)))
