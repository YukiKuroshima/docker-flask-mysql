# project/__init__.py


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


# instantiate the db
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # Use flask-uploads to upload and get images

    app.config['UPLOADED_PHOTOS_DEST'] = '/'

    patch_request_class(app)
    configure_uploads(app, photos)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from server.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
