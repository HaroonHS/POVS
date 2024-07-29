from db import db

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(100), nullable= False, unique = True)
    status = db.Column(db.Integer)
    

    review = db.relationship("ReviewModel", back_populates= "category")