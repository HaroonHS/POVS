from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), nullable= False , unique=True)
    first_name = db.Column(db.String(80), nullable= False)   
    last_name = db.Column(db.String(80), nullable= False)
    email = db.Column(db.String(80), nullable= False, unique=True)
    password = db.Column(db.String(526), nullable= False)
    phone_number = db.Column(db.String(20))
    city = db.Column(db.String(20))
    desc = db.Column(db.String(1024))
    profile_pic = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    country = db.Column(db.String(30))
    region = db.Column(db.String(30))
    client_city = db.Column(db.String(30))
    client_ip = db.Column(db.String(30))
    status = db.Column(db.Integer)
    dob  = db.Column(db.Date)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    last_login = db.Column(db.TIMESTAMP)
    device_token = db.Column(db.String(526))
    code= db.Column(db.String(10))


    reviews = db.relationship("ReviewModel", back_populates= "user", lazy="dynamic", cascade="all, delete" )

    like = db.relationship("ReviewModel", back_populates= "likes", secondary ="likes" , cascade="all, delete")

    taged = db.relationship("ReviewModel", back_populates= "tag_user", secondary ="taged_users", cascade="all, delete")


    #supporters = db.relationship("SupporterModel", back_populates= "user", lazy="dynamic", cascade="all, delete" )