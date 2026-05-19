from flask import Flask
from celery.schedules import crontab

from application.config import LocalDevelopmentConfig
from application.factory import (
    db, api, jwt, cors, cache
)
from application.dummy_data import data_creation
from application.celery import celery_init_app
from application.tasks import drives_cleanup, mail_all_students


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    api.init_app(app)
    from application.api.auth import auth
    api.register_blueprint(auth)
    from application.api.utils import utils
    api.register_blueprint(utils)
    from application.api.student import students
    api.register_blueprint(students)
    from application.api.company import company
    api.register_blueprint(company)
    from application.api.drive import drives
    api.register_blueprint(drives)
    from application.api.applied import applications
    api.register_blueprint(applications)
    from application.api.placement import placements
    api.register_blueprint(placements)
    from application.api.analytics import analytics
    api.register_blueprint(analytics)
    from application.api.download import downloads
    api.register_blueprint(downloads)

    cors.init_app(app, resources={
        r"/*": {
            'origins': ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
            'supports_credentials': True
        }
    })

    app.app_context().push()
    return app


app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'),
        mail_all_students.s(),
        name='Mail all students every 2 minutes'
    )
    sender.add_periodic_task(
        crontab(hour=0, minute=5),
        drives_cleanup.s(),
        name='Clean up old drives daily'
    )


with app.app_context():
    data_creation()

if __name__ == "__main__":
    app.run(debug=True, port=3000)
