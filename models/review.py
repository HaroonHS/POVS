from db import db

class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key = True)
    brandname = db.Column(db.String(80), nullable= False)
    product = db.Column(db.String(100), nullable= False)
    review = db.Column(db.String(256), nullable= False)
    type = db.Column(db.String(50), nullable= False)
    rating  = db.Column(db.Integer, nullable= False)
    country = db.Column(db.String(30))
    region = db.Column(db.String(30))
    client_city = db.Column(db.String(30))
    client_ip = db.Column(db.String(30))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)
    category_id = db.Column(db.Integer,db.ForeignKey("categories.id"), nullable= False)
    status = db.Column(db.Integer)
    is_report = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    user = db.relationship("UserModel", back_populates= "reviews")

    category = db.relationship("CategoryModel", back_populates= "review")

    likes = db.relationship("UserModel", back_populates= "like", secondary ="likes")

    files = db.relationship("FilesModel", back_populates= "review", lazy="dynamic", cascade="all, delete, delete-orphan")

    tag_user = db.relationship("UserModel", back_populates= "taged", secondary ="taged_users")


    reported_by = db.relationship("ReportModel", back_populates= "reviews", lazy="dynamic", cascade="all, delete, delete-orphan")