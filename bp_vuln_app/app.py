import os
from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "files"))
os.makedirs(BASE_DIR, exist_ok=True)

@app.route("/")
def home():
    return "Server running. Use /read?file=filename"

def safe_join(base, user_path):
    full_path = os.path.abspath(os.path.join(base, user_path))
    if not full_path.startswith(base + os.sep):
        raise ValueError("Path traversal detected")
    return full_path

@app.route("/read")
def read_file():
    filename = request.args.get("file")

    if not filename:
        return "Provide ?file=", 400

    try:
        safe_path = safe_join(BASE_DIR, filename)

        with open(safe_path, "r") as f:
            return f.read()

    except ValueError:
        return "Access denied", 403
    except FileNotFoundError:
        return "File not found", 404
    except Exception:
        return "Internal server error", 500