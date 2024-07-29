from db import db

class SupporterModel(db.Model):
    __tablename__ = "supporters"

    id = db.Column(db.Integer, primary_key = True)
    suppoter_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)

    #user = db.relationship("UserModel", back_populates= "supporters")