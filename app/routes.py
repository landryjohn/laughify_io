from app import app

@app.route("/")
@app.route("/random_joke")
def index():
    return "Salut le monde"