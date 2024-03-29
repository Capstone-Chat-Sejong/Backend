#app initial setting
#key, DB connect (secret key)
import os
from flask import Flask
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from datetime import timedelta
from . import db
from dotenv import load_dotenv

load_dotenv()

socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*"
)

def create_app(debug=False):
    app = Flask(__name__)  
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('ACCESS_EXPIRES')))
#    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('REFRESH_EXPIRES')))

    jwt = JWTManager(app)

    #DB connect
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from api.events import ChatNamepsace
    socketio.on_namespace(ChatNamepsace('/chat'))

    from api.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app