from flask import render_template
from .app import app

@app.route('/')
@app.route('/index/')
def index():
    return render_template("nav_bar.html")

if __name__ == "__main__":
    app.run()