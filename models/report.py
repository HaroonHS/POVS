from db import db

class ReportModel(db.Model):
    __tablename__ = "review_report"

    id = db.Column(db.Integer, primary_key = True)
    review_id = db.Column(db.Integer,db.ForeignKey("reviews.id"), nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)


    reviews = db.relationship("ReviewModel", back_populates= "reported_by")
