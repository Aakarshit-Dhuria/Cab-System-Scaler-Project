import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from application.database import db
from application.config import LocalDevelopmentConfig
from application import workers

app = None
api = None


def create_app():
    app = Flask(__name__, template_folder="templates", static_url_path="/static/images")

    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Staring Local Development")
        app.config.from_object(LocalDevelopmentConfig)

    # cache.init_app(app)
    CORS(app)
    db.init_app(app)
    api = Api(app)
    # sec.init_app(app, user_datastore)
    app.app_context().push()

    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        result_expires=3600,
        enable_utc=False,
        timezone="Asia/Calcutta",
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    return app, api, celery


app, api, celery = create_app()

# ************************* Celery Setup **************************


# Add all restful controllers
from application.api import TripTimeAPI, AddBookingsAPI, CabDetailsAPI, AvailableCabsAPI,CitiesAPI

api.add_resource(TripTimeAPI, "/api/get-time")
api.add_resource(CitiesAPI, "/api/get-cities")
api.add_resource(AddBookingsAPI, "/api/add-booking")
api.add_resource(CabDetailsAPI, "/api/cabs", "/api/cabs/<int:cabId>")
api.add_resource(AvailableCabsAPI, "/api/available-cabs")

if __name__ == "__main__":
    app.run(port=8000)
