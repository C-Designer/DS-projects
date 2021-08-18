from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
    app.config['DEBUG'] = True

    if config is not None:
        app.config.update(config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    from flask_app.views import (main_views, member_views, trainer_views, sale_views, predict_views)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(member_views.bp, url_prefix='/api')
    app.register_blueprint(trainer_views.bp, url_prefix='/api')
    app.register_blueprint(sale_views.bp, url_prefix='/api')
    app.register_blueprint(predict_views.bp, url_prefix='/api')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)