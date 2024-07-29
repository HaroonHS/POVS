import os
from ip2geotools.databases.noncommercial import DbIpCity
from random import randint
from datetime import datetime
from flask import request,url_for,redirect,session,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jti,get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from db import db
from models import UserModel,ReviewModel,SupporterModel,MessageModel,ApplicationModel

from schemas import Userschema, UserUpdateSchema,UserLoginSchema,ReviewSchema,SupporterSchema,UserFilterSchema,MessageSchema,ChangePasswordSchema,ForgotPasswordSchema,AppVersionSchema
from flask_mail import Message,Mail
from authlib.integrations.flask_client import OAuth
from marshmallow import Schema, fields, validate,ValidationError,post_load


mail= Mail()

blp = Blueprint("users",__name__,description="Operation on users")

@blp.route("/users/<int:page>")
class UserList(MethodView):
    @jwt_required() ## accept Refresh access token
    @blp.response(200,Userschema(many=True))
    def get(self,page):
        per_page= 5
        users = UserModel.query.filter(UserModel.status == 1).paginate(page=page,per_page=per_page)
        #users = UserModel.query.paginate(page=page,per_page=per_page)
        user_data = Userschema(many=True)
        res_data = user_data.dump(users)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
        
    
@blp.route("/register")
class UserAdd(MethodView):    
    @blp.arguments(Userschema)
    #@blp.response(200,Userschema)
    def post(self,user_data):
        date = datetime.now()
        ip = '180.252.167.171'
        ip_location = DbIpCity.get(ip,api_key="free")
        client_country = ip_location.country
        client_region = ip_location.region
        client_city =  ip_location.city
        client_ip =  ip
        user = UserModel(
                         first_name = user_data['first_name'],
                         last_name = user_data['last_name'],
                         user_name = user_data['user_name'],
                         email = user_data['email'],
                         password = pbkdf2_sha256.hash(user_data['password']), 
                         status = 1,
                         created_at = date, #date.strftime("%d-%m-%y %H:%M:%S"),
                         country = client_country,
                         region = client_region,
                         client_city = client_city,
                         client_ip = client_ip                    
                         )
        try :
             db.session.add(user)
             db.session.commit()
             data_dump = Userschema()
             res_data = data_dump.dump(user)
             app_ver = ApplicationModel.query.get(1)
             status = app_ver.status
        # except ValidationError as e :
        #       print(e)
        except IntegrityError as e:
             #print("illustate sqlalchemy exception raised: %s" % e)
             return jsonify({"status": 400, "message": "User  already Exists" , "body":{}, "error" : {}, "update_available" : ""}),400
             
        except SQLAlchemyError as e:
            
            #print("illustate sqlalchemy exception raised: %s" % e)
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500

        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    

@blp.route("/profile/<string:user_id>")
class Profile(MethodView):
    @blp.response(200,Userschema)
    def get(self, user_id):
         user = UserModel.query.get_or_404(user_id)
         data_dump = Userschema()
         res_data = data_dump.dump(user)
         app_ver = ApplicationModel.query.get(1)
         status = app_ver.status
         return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    
    #@blp.arguments(UserUpdateSchema)
    #@blp.response(200,UserUpdateSchema)
    #@post_load
    def put(self, user_id):
        # form = request.form
        # data_dump = UserUpdateSchema()
        # user = data_dump.load(form)
        date = datetime.now()
        profile = request.files['profile_pic']
        p_img = profile.filename
        p_img = p_img.replace(" ", "_")
        first_name =  request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        gender = request.form['gender']
        city = request.form['city']
        desc = request.form['desc']
        phone_number =request.form['phone_number']
        if not first_name:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        if not user_name:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        if not last_name:
            return (jsonify({"status":422, "message":"Mising Parameters", "body" : {}, "error" : "Missing Error","update_available" : ""}),422)
        user = UserModel.query.get_or_404(user_id)
        if user :
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.user_name = user_name
            user.gender = gender
            user.city = city
            user.desc = desc
            user.updated_at = date #date.strftime("%d-%m-%y %H:%M:%S")
            if p_img :
                    dice = os.path.join('uploads/profile/',p_img)
                    profile.save(dice)
                    user.profile_pic = p_img
             
        #else :
            # user = UserModel(id=user_id,**user_data)
            # user = UserModel(
            #              first_name = user_data['first_name'],
            #              last_name = user_data['last_name'],
            #              user_name = user_data['user_name'],
            #              email = user_data['email'],
            #              password = pbkdf2_sha256.hash(user_data['password']), 
            #              status = 1,
            #              created_at = date.strftime("%d-%m-%y %H:%M:%S")                   
            #              )
        try :
                db.session.add(user)
                db.session.commit()
                data_dump = Userschema()
                res_data = data_dump.dump(user)
                app_ver = ApplicationModel.query.get(1)
                status = app_ver.status
        except IntegrityError :
            return jsonify({"status": 400, "message": "User  already Exists" , "body":{}, "error" : {}, "update_available" : ""}),400
        except SQLAlchemyError :
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
        
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200

        
    
@blp.route("/user/<string:user_id>")
class UserDel(MethodView):
    # @blp.response(200,Userschema)
    # def get(self, user_id):
    #      user = UserModel.query.get_or_404(user_id)
    #      data_dump = Userschema()
    #      res_data = data_dump.dump(user)
    #      return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : ""}),200
    @jwt_required(fresh=True)  ## accept access token not refesh access token
    def delete(self, user_id):
       user = UserModel.query.get_or_404(user_id)
       user.status = 0
       try:
            db.session.add(user)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status
       except IntegrityError :
            return jsonify({"status": 400, "message": "Operation failed" , "body":{}, "error" : {}, "update_available" : ""}),400
       except SQLAlchemyError :
            return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
       
       return jsonify({"status": 200, "message": "Deleted Successfull" , "body":{}, "error" : {},"update_available" : status}),200
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    #@blp.response(UserLoginSchema)
    def post(self,user_data):
        date = datetime.now()
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password ):


            user.last_login = date
            #user.last_login = date.strftime("%d-%m-%y %H:%M:%S")
            try:
                db.session.add(user)
                db.session.commit()
                app_ver = ApplicationModel.query.get(1)
                status = app_ver.status
            except SQLAlchemyError :
                return jsonify({"status": 500, "message": "An Error Occured" , "body":{}, "error" : {},"update_available" : ""}),500
            access_tocken = create_access_token(identity=user.id,fresh=True)
            refresh_access_token = create_refresh_token(identity=user.id)

            #return { "access_token": access_tocken}

            res_data = {
                "email": user.email,
                "id": user.id,
                "access_token": access_tocken,
                "refresh_access_token": refresh_access_token
            }
            #return data
            return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200        #abort(401,message="Invalid Credntials" ,   body={})
        res_data = {"status": 401,"message" : "Invalid Credntials", "body":{},"error" : {},"update_available" : ""},401
        return res_data

@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        
        res_data = { "access_token": new_token}
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
 

# @blp.route("/logout")
# class UserLogout(MethodView):
#     @jwt_required()
#     def post(self):
#         jti = get_jti()["jti"]
#        # BLOCKLIST.add(jti)
#         return {"message": "Logout Successfully."}
    

@blp.route("/filteruser/<int:page>")
class Filters(MethodView):
    @blp.arguments(UserFilterSchema)
    @blp.response(200,Userschema(many=True))
    def post(self,filter_data,page):
        per_page= 5
        search = filter_data['search']
        searchs = "%{}%".format(search)
        user = UserModel.query.filter(or_(UserModel.first_name.ilike(searchs), UserModel.last_name.ilike(searchs),UserModel.user_name.ilike(searchs))).paginate(page=page,per_page=per_page)
        user_data = Userschema(many=True)
        res_data = user_data.dump(user)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    
@blp.route("/supporter/<user_id>")
class GetSupporter(MethodView):
    #@blp.response(200,Userschema(many=True))
    def get(self,user_id):
        followers = db.session.query(UserModel).join(SupporterModel,onclause=UserModel.id == SupporterModel.suppoter_id ).filter(SupporterModel.user_id == user_id)
        data_dump = Userschema(many=True)
        res_data = data_dump.dump(followers)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        #return followers
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
   

@blp.route("/add_supporter")
class AddSupporter(MethodView):
    @blp.arguments(SupporterSchema)
    def post(self,support_data):
        data = SupporterModel(**support_data)
        try :
            db.session.add(data)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status

        except SQLAlchemyError :
            #abort(500,message= "error")
            return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
        return jsonify({"status": 200, "message": "Supporter added successfully" , "body":{}, "error" : {},"update_available" : status}),200
    

@blp.route("/add_message")
class AddMessage(MethodView):
    @blp.arguments(MessageSchema)
    def post(self,message_data):
        date = datetime.now()
        data = MessageModel(**message_data,status=1,is_read=0,created_at=date)
        #data = MessageModel(**message_data,status=1,is_read=0,created_at=date.strftime("%d-%m-%y %H:%M:%S"))
        try :
            db.session.add(data)
            db.session.commit()
            app_ver = ApplicationModel.query.get(1)
            status = app_ver.status

        except SQLAlchemyError :
            #abort(500,message= "error")
            return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
        return jsonify({"status": 200, "message": "message sent successfully" , "body":{}, "error" : {},"update_available" : status}),200
    

@blp.route("/message/<user_id>")
class GetMessage(MethodView):
    #@blp.response(200,Userschema(many=True))
    def get(self,user_id):
        messages = db.session.query(MessageModel).join(UserModel,onclause=UserModel.id == MessageModel.to_user ).filter(MessageModel.to_user == user_id)
        data_dump = MessageSchema(many=True)
        res_data = data_dump.dump(messages)
        app_ver = ApplicationModel.query.get(1)
        status = app_ver.status
        #return followers
        return jsonify({"status": 200, "message": "Success" , "body":res_data, "error" : {},"update_available" : status}),200
    

@blp.route("/change_password")
class ChangePassword(MethodView):
    @blp.arguments(ChangePasswordSchema)
    #@blp.response(UserLoginSchema)
    def post(self,user_data):
        date = datetime.now()
        user = UserModel.query.filter(UserModel.id == user_data['user_id']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password ):

            user.password = pbkdf2_sha256.hash(user_data['new_password'])
            user.updated_at = date #date.strftime("%d-%m-%y %H:%M:%S")
            try :
                db.session.add(user)
                db.session.commit()
                app_ver = ApplicationModel.query.get(1)
                status = app_ver.status
            except SQLAlchemyError :
                return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
            res_data = {
                "id": user.id,
            }
            return jsonify({"status": 200, "message": "Password updated successfully " , "body":res_data, "error" : {},"update_available" : status}),200
        return jsonify({"status": 401,"message" : "Invalid Credntials", "body":{},"error" : {},"update_available" : ""}),401
    
@blp.route("/forgot_password")
class ForgotPassword(MethodView):
    @blp.arguments(ForgotPasswordSchema)
    #@blp.response(UserLoginSchema)
    def post(self,user_data):
        code = randint(100000,1000000)
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()
        if user :
            try :
                    user.code = code
                    db.session.add(user)
                    db.session.commit()
                    app_ver = ApplicationModel.query.get(1)
                    status = app_ver.status

                    subject = "Varification Email"
                    recipients= ["haroon.ssuet@gmail.com","haroonsaeed.ssuet@gmail.com"]
                    sender= "haroon.ssuet@gmail.com"
                    body="\nHi, \nyour varification code is " + str(code)
                    send = sendmail(subject,recipients,sender,body)
                    if send:
                        return jsonify({"status": 200, "message": "Otp send successfully " , "body":{}, "error" : {},"update_available" : status}),200
                    else :
                        return jsonify({"status": 401,"message" : "mail not sent", "body":{},"error" : {},"update_available" : ""}),401
 
                    # msg = Message(
                    #                 subject = "Varification Email",
                    #                 recipients= ["haroon.ssuet@gmail.com","haroonsaeed.ssuet@gmail.com"],
                    #                 sender= "haroon.ssuet@gmail.com"
                    #                 )
                    # msg.body="\nHi, \nyour varification code is " + str(code)
                    # try: 
                    #     mail.send(msg)
                    #     return jsonify({"status": 200, "message": "Otp send successfully " , "body":{}, "error" : {},"update_available" : ""}),200
                    # except Exception as e:
                    #         #print (e)
                    #         #return {"message" : f"mail not sent{e}"}
                    #         return jsonify({"status": 401,"message" : f"mail not sent{e}", "body":{},"error" : {},"update_available" : ""}),401
            except SQLAlchemyError :
                return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500    
        else:
                return jsonify({"status": 401,"message" : "Invalid Credntials", "body":{},"error" : {},"update_available" : ""}),401
        #return jsonify({"status": 200, "message": "Otp send successfully " , "body":{}, "error" : {},"update_available" : ""}),200
    

@blp.route("/reset_password")
class ResetPassword(MethodView):
    @blp.arguments(ForgotPasswordSchema)
    #@blp.response(UserLoginSchema)
    def post(self,user_data):
        date = datetime.now()
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user and user_data['otp'] == user.code :

            user.password = pbkdf2_sha256.hash(user_data['new_password'])
            user.updated_at = date    #date.strftime("%d-%m-%y %H:%M:%S")
            user.code = ''
            try :
                db.session.add(user)
                db.session.commit()
                app_ver = ApplicationModel.query.get(1)
                status = app_ver.status
            except SQLAlchemyError :
                return jsonify({"status": 500, "message": "Failed Internal Server Error" , "body":{}, "error" : {},"update_available" : ""}),500
            res_data = {
                "id": user.id,
            }
            return jsonify({"status": 200, "message": "Password updated successfully " , "body":res_data, "error" : {},"update_available" : status}),200
        return jsonify({"status": 401,"message" : "Invalid otp", "body":{},"error" : {},"update_available" : ""}),401
    


def sendmail(subject,recipients,sender,body):
        msg = Message(
                        subject = subject,
                        recipients= recipients,
                        sender= sender
                        )
        msg.body=body
        try: 
            mail.send(msg)
            return True
            #return jsonify({"status": 200, "message": "email send successfully " , "body":{}, "error" : {},"update_available" : ""}),200
        except Exception as e:
            return False
            #print (e)
            #return {"message" : f"mail not sent{e}"}
            #return jsonify({"status": 401,"message" : f"mail not sent{e}", "body":{},"error" : {},"update_available" : ""}),401

@blp.route("/update_app_version")
class AppVersion(MethodView):
    @blp.arguments(AppVersionSchema)
    #@blp.response(200,UserUpdateSchema)
    def put(self, app_data):
        date = datetime.now()
        version = ApplicationModel.query.get(app_data['id'])
        if version :
            version.name = app_data['name']
            version.status = app_data['status']
            version.version = app_data['version']
            version.updated_at = date # date.strftime("%d-%m-%y %H:%M:%S")
        else :
            version = ApplicationModel(**app_data,created_at=date)
            #version = ApplicationModel(**app_data,created_at=date.strftime("%d-%m-%y %H:%M:%S"))

        db.session.add(version)
        db.session.commit()
        return jsonify({"message":"Application version updated"}),200
    
### for later stage when user delete their accounts after 30 days we delete  that permanently
# @blp.route("/permanent_delete_User")
# class PermanenetDelUsr(MethodView):
#     def delete(self):
#         Users = UserModel.query.filter(UserModel.status == 0)
#         for User in Users:
#             sp = SupporterModel.query.filter(or_(SupporterModel.user_id == User.id , SupporterModel.suppoter_id == User.id))
#             for u in sp :
#                 db.session.delete(u.id)
#                 db.session.commit()
#             print (User.id)
#             db.session.delete(User)
#             db.session.commit()
#         app_ver = ApplicationModel.query.get(1)
#         status = app_ver.status        
#         return jsonify({"status": 200, "message": "Deleted Successfull" , "body":{}, "error" : {},"update_available" : status}),200
      
    
        
    

       

             
