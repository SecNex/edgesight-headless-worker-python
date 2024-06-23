from typing import Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from headless import Website

class API:
    def __init__(self, headless, database):
        self.app = Flask(__name__)
        self.headless = headless
        self.database = database
        self.socket = SocketIO(self.app, debug=True, cors_allowed_origins="*", async_mode="threading")
        CORS(self.app)

        self.headless.add_websites(self.get_websites())

        @self.app.route("/", methods=["GET"])
        def index():
            return jsonify({
                "status": "running",
                "version": "1.0.0"
            })

        @self.app.route("/headless", methods=["GET"])
        def get_websites():
            return jsonify(self.get_websites())

        @self.app.route("/headless", methods=["POST"])
        def post_website():
            url, timeout, delay, delay_time = self.check_website(request.json.get("url"), request.json.get("timeout"), request.json.get("delay"), request.json.get("delay_time"))
            if not url:
                return url, timeout
            return self.add_website(url, timeout, delay, delay_time)

        @self.socket.on("connect")
        def connect():
            print("[SOCKET] Connected!")

        @self.socket.on("disconnect")
        def disconnect():
            print("[SOCKET] Disconnected!")

        @self.socket.on("screenshot")
        def screenshot(website_id):
            website = self.database.fetch("SELECT * FROM websites WHERE id = %s", (website_id,))
            if not website:
                emit("error", "Website not found!")
                return
            __screenshot_as_base64 = self.headless.get_screenshot_as_base64(Website(website[1], website[2], website[3], website[4]))
            emit("screenshot", __screenshot_as_base64)
            self.socket.sleep(1)

    def check_website(self, url: str, timeout: int, delay: bool, delay_time: int) -> Tuple[str, int, bool, int]:
        if not url:
            return "URL cannot be empty!", 400, False, 0
        if not timeout:
            return "Timeout cannot be empty!", 400, False, 0
        if not delay:
            return "Delay cannot be empty!", 400, False, 0
        if not delay_time:
            return "Delay time cannot be empty!", 400, False, 0
        return url, timeout, delay, delay_time
    
    def exists(self, url: str) -> bool:
        websites = self.get_websites()
        for website in websites:
            if website.url == url:
                return True
        return False
    
    def add_website(self, url: str, timeout: int, delay: bool, delay_time: int):
        if self.exists(url):
            return "Website already exists!", 400
        self.database.execute("INSERT INTO websites (url, timeout, delay, delay_time) VALUES (%s, %s, %s, %s)", (url, timeout, delay, delay_time))
        website = Website(url, timeout, delay, delay_time)
        self.headless.add_website(website)
        return jsonify({
            "url": url,
            "timeout": timeout,
            "delay": delay,
            "delay_time": delay_time
        }), 201

    def get_websites(self):
        websites = self.database.fetch("SELECT * FROM websites")
        print(websites)
        __websites = []
        for website in websites:
            __websites.append(Website(website[1], website[2], website[3], website[4]))
        if not __websites:
            return []
        return __websites

    def run(self, host: str = "localhost", port: int = 5000, debug: bool = False):
        self.app.run(host=host, port=port, debug=debug)