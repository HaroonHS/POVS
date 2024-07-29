from db import db

class TagUsersModel(db.Model):
    __tablename__ = "taged_users"

    id = db.Column(db.Integer, primary_key = True)
    review_id = db.Column(db.Integer,db.ForeignKey("reviews.id"), nullable= False)
    tuser_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)

    #user = db.relationship("UserModel", back_populates= "supporters")