import uuid
from datetime import datetime
from flask import request,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jwt_identity
from schemas import NotificationSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import UserModel,NotificationModel,ApplicationModel


blp = Blueprint("notification", __name__,description="Operation on notification")
    
@blp.route("/notification/<user_id>")
class GetSupporter(MethodView):
    @jwt_required()
    #@blp.response(200,Userschema(many=True))
    def get(self,user_id):
        noti = db.session.query(NotificationModel).join(UserModel,onclause=UserModel.id == NotificationModel.user_id ).filter(NotificationModel.user_id == user_id).all()
        data_dump = NotificationSchema(many=True)
        res_data = data_dump.dump(noti)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        #return followers
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
   

@blp.route("/add_notification")
class AddSupporter(MethodView):
    @jwt_required()
    @blp.arguments(NotificationSchema)
    def post(self,noti_data):
        date = datetime.now()
        data = NotificationModel(**noti_data,created_at = date ,status = 1,is_sent = 0)
        #data = NotificationModel(**noti_data,created_at = date.strftime("%d-%m-%y %H:%M:%S") ,status = 1,is_sent = 0)
        try :
            db.session.add(data)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status

        except SQLAlchemyError :
            #abort(500,message= "error")
            return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
        return jsonify({"status": 200, "message": "Notification added successfully" , "body":{}, "error" : {},"update_available" : status}),200
    

