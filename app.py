from flask import Flask, render_template
from database import init_db
from backend.api import api
from backend.config import settings


init_db()


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=settings.DEBUG)
