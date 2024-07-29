from db import db

class ApplicationModel(db.Model):
    __tablename__ = "apps"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(512), nullable= False)
    status = db.Column(db.String(5))
    version = db.Column(db.String(5))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    