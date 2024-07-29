
import os
from flask import Flask,jsonify,redirect,url_for,session,make_response
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta

from db import db
import models
from resources.category import blp as CategoryBlueprint
from resources.user import blp as UserBlueprint
from resources.review import blp as ReviewBlueprint
from resources.notification import blp as NotificationBlueprint
from flask_mail  import Mail , Message
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate

def create_app(db_url=None):
    app = Flask(__name__)
    app.secret_key =" haroon saeed"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Povs REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")  ## chnge date format in app
    #app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost/pov_api")
    app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_SECRET_KEY"] = "Haroon"

    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "haroon.ssuet@gmail.com"
    app.config["MAIL_PASSWORD"] = "hjiuiszbrnfrxdev"
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
   
    mail = Mail(app)
   
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    #oath = OAuth(app)

    oath = OAuth()
    oath.init_app(app)

    google = oath.register(
            name = 'google',
            client_id = '',          
            client_secret='',
            access_token_url ='https://accounts.google.com/o/oauth2/token',
            access_token_params = None,
            authorize_url ='https://accounts.google.com/o/oauth2/auth',
            authorize_params = None,
            api_base_url = 'https://www.googleapis.com/oauth2/v1/',
            client_kwargs={'scope': 'openid profile email'},
            jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
            )
    
    jwt = JWTManager(app)

    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message":"Token has been revoked.", "error" : "token_revoked", "update_available" : "", "status": 401,"body":{}}),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"message":"The token has expired.", "error":"expired_token","update_available" : "", "status": 401,"body":{}}),
            401,
            )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
               jsonify({"message":"Signature verification failed.", "error": "Invalid_token", "update_available" : "", "status": 401,"body":{}}),
               401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message":"Request does not contain an access token.", "error" : "authorization_required", "update_available" : "", "status": 401,"body":{}}),
            401,
        )

    @app.errorhandler(404)
    def handle_404_error(_error):
        return make_response(jsonify({"status":404, "message":"Request failed, not found.", "body" : {}, "error" : "Not Found Error","update_available" : ""}),404)
    
    @app.errorhandler(422)
    def handle_422_error(_error):
        return make_response(jsonify({"status":422, "message":print("illustate sqlalchemy exception raised: %s" % _error), "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
    

    @app.errorhandler(401)
    def handle_401_error(_error):
        return make_response(jsonify({"status":401, "message":"Failed bad request", "body" : {}, "error" : "Bad Error","update_available" : ""}),401)
    
    @app.errorhandler(500)
    def handle_500_error(_error):
        return make_response(jsonify({"status":500, "message":"Failed interal server error.", "body" : {}, "error" : "server Error","update_available" : ""}),500)
    
    @app.errorhandler(400)
    def handle_400_error(_error):
        return make_response(jsonify({"status":400, "message":"Already Exsist", "body" : {}, "error" : "Integrity Error","update_available" : ""}),400)
    
    
  
    # @app.route("/")
    # def hello_world():
    #     email = "hiiii" 
    #     return f'hello, {email}'
    

    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ReviewBlueprint)
    api.register_blueprint(NotificationBlueprint)
    
   

    return app




