import json
import logging
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, messaging
from flask import Flask, jsonify, request

APP_VERSION = "0.2.0"
SERVICE_ACCOUNT_PATH = Path("/config/firebase-service-account.json")
OPTIONS_PATH = Path("/data/options.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("digital-eye-gateway")
app = Flask(__name__)


def load_options():
    try:
        with OPTIONS_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return {}
    except Exception:
        log.exception("Failed to read Home Assistant app options")
        return {}


OPTIONS = load_options()
API_KEY = str(OPTIONS.get("api_key", "")).strip()

FIREBASE_READY = False
FIREBASE_ERROR = None


def init_firebase():
    global FIREBASE_READY, FIREBASE_ERROR

    if firebase_admin._apps:
        FIREBASE_READY = True
        FIREBASE_ERROR = None
        return

    if not SERVICE_ACCOUNT_PATH.is_file():
        FIREBASE_ERROR = f"Missing {SERVICE_ACCOUNT_PATH}"
        log.warning("Firebase credentials not found at %s", SERVICE_ACCOUNT_PATH)
        return

    try:
        cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
        firebase_admin.initialize_app(cred)
        FIREBASE_READY = True
        FIREBASE_ERROR = None
        log.info("Firebase Admin SDK initialized")
    except Exception as exc:
        FIREBASE_ERROR = str(exc)
        log.exception("Firebase Admin SDK initialization failed")


init_firebase()


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        version=APP_VERSION,
        firebase_ready=FIREBASE_READY,
        api_key_configured=bool(API_KEY),
    )


@app.post("/api/test-push")
def test_push():
    if not API_KEY:
        return jsonify(error="api_key is not configured"), 503

    if request.headers.get("X-API-Key", "") != API_KEY:
        return jsonify(error="unauthorized"), 401

    if not FIREBASE_READY:
        return jsonify(error="firebase_not_ready", detail=FIREBASE_ERROR), 503

    payload = request.get_json(silent=True) or {}

    token = str(payload.get("token", "")).strip()
    if not token:
        return jsonify(error="token is required"), 400

    title = str(payload.get("title", "Digital Eye"))
    body = str(payload.get("body", "Test notification"))

    raw_data = payload.get("data") or {}
    if not isinstance(raw_data, dict):
        return jsonify(error="data must be an object"), 400

    data = {str(key): str(value) for key, value in raw_data.items()}

    try:
        msg = messaging.Message(
            token=token,
            notification=messaging.Notification(title=title, body=body),
            data=data,
            android=messaging.AndroidConfig(priority="high"),
        )
        message_id = messaging.send(msg)
        log.info("Test FCM message sent successfully")
        return jsonify(status="sent", message_id=message_id)
    except Exception as exc:
        log.exception("FCM send failed")
        return jsonify(error="fcm_send_failed", detail=str(exc)), 502
