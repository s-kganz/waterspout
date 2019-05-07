import dbconfig
from dbconfig import maps_key as maps_key

# Only import the non-mock helper if not testing
if dbconfig.test:
    from dbhelper import MockHelper as DBHelper
else:
    from dbhelper import DBHelper 

from flask import Flask, render_template, request

app = Flask(__name__)
DB = DBHelper()

@app.route('/')
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html", data=data, maps_key=maps_key)

@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    