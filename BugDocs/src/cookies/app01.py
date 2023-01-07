from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.get("/")
def home():
    response = make_response(render_template("index.html", title="cookies 测试"))
    response.set_cookie("cookies_name", "i am cookies running 5001")
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 5001, True)
