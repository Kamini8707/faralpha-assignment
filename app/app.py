from datetime import datetime
import os
from urllib.parse import quote_plus
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


def get_mongo_uri():
    # Use full MONGODB_URI if explicitly provided, otherwise construct from credentials
    mongo_uri = os.environ.get("MONGODB_URI")
    if mongo_uri:
        return mongo_uri

    username = os.environ.get("MONGO_USER")
    password = os.environ.get("MONGO_PASSWORD")
    host = os.environ.get("MONGO_HOST", "localhost")
    port = os.environ.get("MONGO_PORT", "27017")
    auth_source = os.environ.get("MONGO_AUTH_SOURCE", "admin")

    if username and password:
        user_encoded = quote_plus(username)
        pass_encoded = quote_plus(password)
        return f"mongodb://{user_encoded}:{pass_encoded}@{host}:{port}/?authSource={auth_source}"

    return f"mongodb://{host}:{port}/"


client = MongoClient(get_mongo_uri(), serverSelectionTimeoutMS=5000)
db = client.flask_db
collection = db.data


@app.route("/")
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        payload = request.get_json(silent=True)
        if not payload:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400
        collection.insert_one(payload)
        return jsonify({"status": "Data inserted"}), 201

    documents = list(collection.find({}, {"_id": 0}))
    return jsonify(documents), 200


@app.route("/health", methods=["GET"])
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as exc:
        return jsonify({"status": "unhealthy", "error": str(exc)}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)