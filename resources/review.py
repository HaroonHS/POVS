import os
from ip2geotools.databases.noncommercial import DbIpCity
from flask import request,jsonify
from flask.views import MethodView
from datetime import datetime
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jti,get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from db import db
from models import ReviewModel,UserModel,FilesModel,TagUsersModel,ApplicationModel,ReportModel

from schemas import ReviewSchema,ReviewLikeSchema,FilterSchema

blp = Blueprint("reviews",__name__,description="Operation on feedback")

@blp.route("/feedback/<int:page>")
class Reviews(MethodView):
    #@blp.response(200,ReviewSchema(many=True))
    def get(self,page):
        per_page= 5
        review = ReviewModel.query.filter(ReviewModel.status == 1).paginate(page=page,per_page=per_page)
        review_data = ReviewSchema(many=True)
        res_data = review_data.dump(review)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status

        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
        #return review
    
@blp.route("/feedback")
class ReviewsAdd(MethodView):
    #@blp.arguments(ReviewSchema)
    #@blp.response(200,ReviewSchema)
    def post(self):
        #ip = request.remote_addr
        #ip = request.environ['REMOTE_ADDR']
        date = datetime.now()
        ip = '180.252.167.171'
        ip_location = DbIpCity.get(ip,api_key="free")
        client_country = ip_location.country
        client_region = ip_location.region
        client_city =  ip_location.city
        client_ip =  ip
        tag_users = request.form.getlist('tag_users')
        uploaded_file = request.files.getlist('file')
        brandname = request.form['brandname']
        product = request.form['product']
        review_desc = request.form['review']
        rating = request.form['rating']
        user_id = request.form['user_id']
        type = request.form['type']
        category = request.form['category']

        if not category:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        if not brandname:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        if not review_desc:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        #formdata = (brandname,product,review_desc,rating,user_id)

        revieww  = ReviewModel(
                            brandname = brandname,
                            product = product,
                            review = review_desc,
                            rating = rating,
                            user_id = user_id,
                            type= type,
                            category_id = category,
                            country = client_country,
                            region = client_region,
                            client_city = client_city,
                            client_ip = client_ip,
                            status = 1,
                            created_at = date #date.strftime("%d-%m-%y %H:%M:%S")        
          )
        try :
            # db.session.add(revieww)
            db.session.add(revieww)
            db.session.commit()
            last_id = revieww.id
            ##for new change
            for user in tag_users:
                t_user  = TagUsersModel(
                                review_id = last_id,
                                tuser_id = user                   
                    )
                
                db.session.add(t_user)
                db.session.commit()
            ## til here
            for file in uploaded_file:
                fname = file.filename
                fname = fname.replace(" ", "_")
                filedata  = FilesModel(
                                review_id = last_id,
                                filename = fname                   
                    )
                
                db.session.add(filedata)
                db.session.commit()
                dice = os.path.join('uploads/',fname)
                file.save(dice)
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status
        except SQLAlchemyError as e:
            print("illustate sqlalchemy exception raised: %s" % e)
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
            #abort(500,message =str(e))
        data_dump = ReviewSchema()
        res_data = data_dump.dump(revieww)
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200


@blp.route("/userfeedback/<int:user_id>")
class UserRviews(MethodView):
    #@blp.response(200,ReviewSchema(many=True))
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        review = user.reviews.all()
        review_data = ReviewSchema(many=True)
        res_data = review_data.dump(review)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status

        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200

@blp.route("/like")
class ReviewLikes(MethodView):
    @blp.arguments(ReviewLikeSchema)
    @blp.response(200,ReviewSchema)
    def post(self,review_data):
        user = UserModel.query.get_or_404(review_data['user_id'])
        Review = ReviewModel.query.get_or_404(review_data['review_id'])

        user.like.append(Review)    

        try:
            db.session.add(user)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status
        except SQLAlchemyError:
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
            #abort(500,message="An error occur ")
            
        review_data = ReviewSchema()
        res_data = review_data.dump(Review)
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    

@blp.route("/feedback_by_id/<int:review_id>")
class UserRviews(MethodView):
    @blp.response(200,ReviewSchema(many=True))
    def get(self,review_id):
        review = ReviewModel.query.filter(ReviewModel.id == review_id)
        review_data = ReviewSchema(many=True)
        res_data = review_data.dump(review)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    

    def delete(self, review_id):
       review = ReviewModel.query.get_or_404(review_id)
       review.status = 0
       try:
            db.session.add(review)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status
       except IntegrityError :
            return jsonify({"status": 400, "message": "Operation failed" , "body":{}, "error" : {}, "update_available" : ""}),400
       except SQLAlchemyError :
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
       
       return jsonify({"status": 200, "message": "Deleted Successfull" , "body":{}, "error" : {},"update_available" : status}),200
    
@blp.route("/filter")
class Filters(MethodView):
    @blp.arguments(FilterSchema) #later on uncomment and add schema
    @blp.response(200,ReviewSchema(many=True))
    def post(self,filter_data):
        search = filter_data['search']
        searchs = "%{}%".format(search)
        brand  =  filter_data['brandname']
        brandname = "%{}%".format(brand)
        type = filter_data['type']
        category = filter_data['category']
        
        if category : 
                review = ReviewModel.query.filter(or_(ReviewModel.brandname.ilike(searchs), ReviewModel.product.ilike(searchs), ReviewModel.brandname.ilike(brandname), ReviewModel.product.ilike(brandname)), ReviewModel.type == type,  ReviewModel.category_id == category).all() # or query
        else :
                review = ReviewModel.query.filter(or_(ReviewModel.brandname.ilike(searchs), ReviewModel.product.ilike(searchs), ReviewModel.brandname.ilike(brandname), ReviewModel.product.ilike(brandname)), ReviewModel.type == type).all()
        star = 0
        onestar = 0
        twostar = 0
        threestar = 0
        fourstar = 0
        fivestar = 0
        counter = 0
        score = 0
        if type == "Review":
            for value in review:
                if value.rating == 1:
                    onestar +=1
                if value.rating == 2:
                    twostar +=1
                if value.rating == 3:
                    threestar +=1
                if value.rating == 4:
                    fourstar +=1
                if value.rating == 5:
                    fivestar +=1
                counter +=1
                star = star + value.rating
                score = star / counter
        summary = {
            "onestar": onestar,
            "twostar":twostar,
            "threestar":threestar,
            "fourstar":fourstar,
            "fivestar":fivestar,
            "score":score
        }
        review_data = ReviewSchema(many=True)
        res_data = review_data.dump(review) 
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        #print(counter)
        return jsonify({"status": 200, "message": "Success" , "body":{"review":res_data,"summary":summary}, "error" : {},"update_available" : status}),200
    

@blp.route("/review_report")
class AddSupporter(MethodView):
    @blp.arguments(ReviewLikeSchema)
    def post(self,report_data):
        date = datetime.now()
        review = ReviewModel.query.filter(ReviewModel.id == report_data['review_id']).first()
        if review:
            # count = review.is_report
            # count +1
            review.is_report +=1
            review.updated_at = date #date.strftime("%d-%m-%y %H:%M:%S")
        data = ReportModel(**report_data,created_at = date)
        #data = ReportModel(**report_data,created_at = date.strftime("%d-%m-%y %H:%M:%S"))
        try :
            db.session.add(data)
            db.session.add(review)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status

        except SQLAlchemyError :
            #abort(500,message= "error")
            return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
        return jsonify({"status": 200, "message": "Review Reported successfully" , "body":{}, "error" : {},"update_available" : status}),200
    

@blp.route("/review_block")
class AddSupporter(MethodView):
    @blp.arguments(ReviewLikeSchema)
    def post(self,report_data):
        date = datetime.now()
        review = ReviewModel.query.filter(ReviewModel.id == report_data['review_id']).first()
        if review:
            review.status = 2
            review.updated_at = date #date.strftime("%d-%m-%y %H:%M:%S")
        try :
            db.session.add(review)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status

        except SQLAlchemyError :
            #abort(500,message= "error")
            return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
        return jsonify({"status": 200, "message": "Review Reported successfully" , "body":{}, "error" : {},"update_available" : status}),200
    

@blp.route("/edit_feedback/<int:review_id>")
class ReviewsAdd(MethodView):
    #@blp.arguments(ReviewSchema)
    #@blp.response(200,ReviewSchema)
    def post(self,review_id):
        feedback = ReviewModel.query.get_or_404(review_id)
        try :
            db.session.delete(feedback)
            db.session.commit()
        except SQLAlchemyError as e:
            print("illustate sqlalchemy exception raised: %s" % e)
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
        #ip = request.remote_addr
        #ip = request.environ['REMOTE_ADDR']
        date = datetime.now()
        ip = '180.252.167.171'
        ip_location = DbIpCity.get(ip,api_key="free")
        client_country = ip_location.country
        client_region = ip_location.region
        client_city =  ip_location.city
        client_ip =  ip
        tag_users = request.form.getlist('tag_users')
        uploaded_file = request.files.getlist('file')
        brandname = request.form['brandname']
        product = request.form['product']
        review_desc = request.form['review']
        rating = request.form['rating']
        user_id = request.form['user_id']
        type = request.form['type']
        category = request.form['category']

        if not category:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        if not brandname:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        if not review_desc:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        #formdata = (brandname,product,review_desc,rating,user_id)
        
        revieww  = ReviewModel(
                            brandname = brandname,
                            product = product,
                            review = review_desc,
                            rating = rating,
                            user_id = user_id,
                            type= type,
                            category_id = category,
                            country = client_country,
                            region = client_region,
                            client_city = client_city,
                            client_ip = client_ip,
                            status = 1,
                            created_at = date, #date.strftime("%d-%m-%y %H:%M:%S"),
                            id = review_id        
          )
        try :
            # db.session.add(revieww)
            db.session.add(revieww)
            db.session.commit()
            last_id = revieww.id
            ##for new change
            for user in tag_users:
                t_user  = TagUsersModel(
                                review_id = last_id,
                                tuser_id = user                   
                    )
                
                db.session.add(t_user)
                db.session.commit()
            ## til here
            for file in uploaded_file:
                fname = file.filename
                fname = fname.replace(" ", "_")
                filedata  = FilesModel(
                                review_id = last_id,
                                filename = fname                   
                    )
                
                db.session.add(filedata)
                db.session.commit()
                dice = os.path.join('uploads/',fname)
                file.save(dice)
            app_ver = ApplicationModel.query.get(1)
            appstatus = app_ver.status
        except SQLAlchemyError as e:
            print("illustate sqlalchemy exception raised: %s" % e)
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
            #abort(500,message =str(e))
        data_dump = ReviewSchema()
        res_data = data_dump.dump(revieww)
        return jsonify({"status": 200, "message": "Feedback updated successfully" , "body":res_data, "error" : {},"update_available" : appstatus}),200

        
### for later stage when user delete their feebdack after 30 days we delete  that permanently
# @blp.route("/permanent_delete")
# class PermanenetDel(MethodView):
#     def delete(self):
#         review = ReviewModel.query.filter(ReviewModel.status == 0)
#         for feed in review:
#             print (feed.id)
#             db.session.delete(feed.id)
#             db.session.commit()
#         app_ver = ApplicationModel.query.get(1)
#         status = app_ver.status        
#         return jsonify({"status": 200, "message": "Deleted Successfull" , "body":{}, "error" : {},"update_available" : status}),200


