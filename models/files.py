from db import db

class FilesModel(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), nullable= False)
    review_id = db.Column(db.Integer,db.ForeignKey("reviews.id"), nullable= False)

    review = db.relationship("ReviewModel", back_populates= "files")