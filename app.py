from flask import Flask, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy.orm import scoped_session, sessionmaker
import os

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = None
try:
    engine = create_engine(DATABASE_URL)
except NoSuchModuleError:
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")
    engine = create_engine(DATABASE_URL)

db = scoped_session(sessionmaker(bind=engine))


@app.route('/<string:code>')
def get_link(code: str):  # put application's code here
    if request.method == "POST":
        return "Invalid Request"

    res_data = db.execute("SELECT * FROM surl WHERE code= :code", {"code": code}).fetchone()

    if res_data is None:
        data = {
            "status": 400,
            "msg": "link not found"
        }
        return jsonify(data), 400

    data = {
        "status": 200,
        "code": res_data[0],
        "link": res_data[1]
    }

    return jsonify(data), 200


if __name__ == '__main__':
    app.run()
