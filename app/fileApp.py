from flask import Flask, request
import time

app = Flask(__name__)  # 实例化应用


@app.route("/file", methods=["GET"])
def query():
    data = request.args
    file_lst = [
        "120", "121", "122", "123", "124"
    ]
    if data["file_id"] in file_lst:
        return {"msg": "success"}, 200
    else:
        return {"msg": "file not exits"}, 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8771, debug=True)
