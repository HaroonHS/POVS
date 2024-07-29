import uuid
from flask import request,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jwt_identity
from schemas import PlainCategorySchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CategoryModel,ApplicationModel


blp = Blueprint("category", __name__,description="Operation on category")
    
@blp.route("/category")
class Cat(MethodView):
    @blp.arguments(PlainCategorySchema)
    @blp.response(200,PlainCategorySchema)
    def post(self, category_data):
        cate =  CategoryModel(**category_data,status = 1)
        try:
            db.session.add(cate)
            db.session.commit()
            user_data = PlainCategorySchema()
            res_data = user_data.dump(cate)
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status
        except IntegrityError as e:
            #print("illustate sqlalchemy exception raised: %s" % e)
            return (jsonify({"status":422, "message":"Already exisit", "body" : {}, "error" : "Integrity Error"}),422)
        except SQLAlchemyError:
            return (jsonify({"status":500, "message":"Internal error", "body" : {}, "error" : "Internal Error"}),500)

        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    
    
    @jwt_required()
    @blp.response(200,PlainCategorySchema)
    def get(self):
        category = CategoryModel.query.all()
        user_data = PlainCategorySchema(many=True)
        res_data = user_data.dump(category)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status

        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    

