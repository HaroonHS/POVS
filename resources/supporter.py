import os
import uuid
from flask import request,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jti,get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from db import db
from models import UserModel,SupporterModel

from schemas import SupporterSchema

blp = Blueprint("reviews",__name__,description="operation on reviews")

@blp.route("/supporter")
class Reviews(MethodView):
    #@blp.response(200,ReviewSchema(many=True))
    def get(self):
        review = SupporterModel.query.all()
        return jsonify(review)
    

    
    @blp.arguments(SupporterSchema)
    #@blp.response(200,ReviewSchema)
    def post(self,review_data):
        review = SupporterModel(**review_data)
        # review  = ReviewModel(
        #                    product = review_data['product'],
                    
        #  )

        try :
            db.session.add(review)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message =str(e))
        return jsonify(review)