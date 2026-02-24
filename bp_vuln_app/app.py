import os
from flask import Flask, request

app = Flask(__name__)

# Base folder (like blueprint root_path)
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "files"))
os.makedirs(BASE_DIR, exist_ok=True)

@app.route("/")
def home():
    return "Server running. Use /read?file=filename"

@app.route("/read")
def read_file():
    filename = request.args.get("file")

    if not filename:
        return "Provide ?file=", 400

    try:
        # 🚨 Vulnerable join (NO SECURITY CHECK)
        file_path = os.path.join(BASE_DIR, filename)

        with open(file_path, "r") as f:
            return f.read()

    except FileNotFoundError:
        return "File not founddd", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
