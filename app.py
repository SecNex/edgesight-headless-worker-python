from api import API
from database import Database
from headless import HeadlessPlayer

import argparse

def start(without_api: bool = False, force: bool = False, timeout: int = 5):
    db = Database()
    db.test()
    if force:
        db.clear()
    db.init()
    if not without_api:
        print("[EDGESIGHT] Starting with API...")
        api = API(database=db, headless=HeadlessPlayer(again_after=timeout))
        api.run()
    else:
        print("[EDGESIGHT] Starting without API...")
        HeadlessPlayer(database=db, again_after=timeout).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Headless Player")
    parser.add_argument("--noapi", action="store_true", help="Do you want to start without api?", dest="noapi")
    parser.add_argument("--force", action="store_true", help="Do you want to clear the database?", dest="force")
    parser.add_argument("--timeout", type=int, help="Timeout for the headless player", default=5)
    args = parser.parse_args()
    start(without_api=args.noapi, force=args.force, timeout=args.timeout)