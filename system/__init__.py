from flask import Flask,render_template,request,redirect,url_for
from system.utils.generate_content import get_files , generate_content
from system.utils.create_queue import create_queue
from dotenv import load_dotenv
from celery import Celery, Task , current_app
from celery.result import AsyncResult
from flask_sqlalchemy import SQLAlchemy
from system.db import db
from system.utils.get_tasks import get_task
load_dotenv(".env")

def celery_init_app(app: Flask) -> Celery:
    create_queue()
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app():
    app = Flask(__name__,template_folder="./views",static_folder="./contents")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.sqlite"
    db.init_app(app)
    with app.app_context():
        db.create_all()

    CELERY_BROKER_BACKEND = "sqla+sqlite:///celery.sqlite"
    CELERY_CACHE_BACKEND = "db+sqlite:///celery.sqlite"
    CELERY_RESULT_BACKEND = "db+sqlite:///celery.sqlite"

    app.config.from_mapping(
    CELERY=dict(
        broker_url=CELERY_BROKER_BACKEND,
        result_backend=CELERY_RESULT_BACKEND,
        task_ignore_result=True,
        result_persistent = True,
        result_extended = True,
        celery_task_track_started = True
    ),
)
    app.config.from_prefixed_env()
    celery_init_app(app)
    app.app_context().push() # pushing context so that celery workers can use it
    # routes
    @app.get("/")
    def main():
        tasks = get_task()
        return render_template("index.html",tasks=tasks)

    @app.post("/generate")
    def generate():
        url = request.form.get("url")    
        company_name = request.form.get("company_name")    
        with app.app_context():
            task_id = generate_content.delay(company_name=company_name,link=url)
            print(task_id)
        return redirect(url_for("main"))

    @app.get("/previous")
    def see_previous():
        inspector = current_app.control.inspect()
        print(inspector.active())
        print(inspector.reserved())
        return render_template("previous.html",content=get_files())

    @app.get("/result/<id>")
    def task_result(id: str) -> dict[str, object]:
        result = AsyncResult(id)
        return {
            "id":result.task_id,
            "ready": result.ready(),
            "state":result.state,
            "kwargs":result.kwargs,
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }
    return app