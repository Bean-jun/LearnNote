from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/")
def home():
    cookies = request.cookies.get("cookies_name")
    return jsonify({"cookies": cookies})


if __name__ == "__main__":
    app.run("0.0.0.0", 5002, True)
