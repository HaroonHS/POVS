from db import db

class LikeModel(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key = True)
    review_id = db.Column(db.Integer,db.ForeignKey("reviews.id"), nullable= False)
    uuser_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)

    #user = db.relationship("UserModel", back_populates= "supporters")