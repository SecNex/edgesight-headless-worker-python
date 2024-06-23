from api import API
from database import Database
from headless import HeadlessPlayer

import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Headless Player")
    parser.add_argument("--noapi", action="store_true", help="Do you want to start without api?", dest="noapi")
    parser.add_argument("--force", action="store_true", help="Do you want to clear the database?", dest="force")
    parser.add_argument("--timeout", type=int, help="Timeout for the headless player", default=5)
    parser.add_argument("--debug", action="store_true", help="Do you want to enable debug mode?", dest="debug", default=False)
    parser.add_argument("--apiport", type=int, help="API port", default=os.getenv("API_PORT", 5000), dest="apiport")
    parser.add_argument("--apihost", type=str, help="API host", default=os.getenv("API_HOST", "localhost"), dest="apihost")
    __db = parser.add_argument_group("Database")
    __db.add_argument("--host", type=str, help="Database host", default=os.getenv("DB_HOST", "localhost"), dest="host")
    __db.add_argument("--port", type=int, help="Database port", default=os.getenv("DB_PORT", 5432), dest="port")
    __db.add_argument("--database", type=str, help="Database name", default=os.getenv("DB_NAME", "postgres"), dest="database")
    __db.add_argument("--user", type=str, help="Database user", default=os.getenv("DB_USER", "postgres"), dest="user")
    __db.add_argument("--password", type=str, help="Database password", default=os.getenv("DB_PASSWORD", "postgres"), dest="password")
    return parser.parse_args()

def start(without_api: bool = False, force: bool = False, timeout: int = 5, db_host: str = "localhost", db_port: int = 5432, db_name: str = "postgres", db_user: str = "postgres", db_password: str = "postgres", api_host: str = "localhost", api_port: int = 5000, debug: bool = False):
    db = Database(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    db.test()
    if force:
        db.clear()
    db.init()
    if not without_api:
        print("[EDGESIGHT] Starting with API...")
        api = API(database=db, headless=HeadlessPlayer(again_after=timeout))
        api.run(host=api_host, port=api_port, debug=debug)
    else:
        print("[EDGESIGHT] Starting without API...")
        HeadlessPlayer(database=db, again_after=timeout).start()

if __name__ == "__main__":
    args = parse_args()
    start(without_api=args.noapi, force=args.force, timeout=args.timeout, db_host=args.host, db_port=args.port, db_name=args.database, db_user=args.user, db_password=args.password, api_host=args.apihost, api_port=args.apiport, debug=args.debug)