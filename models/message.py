from db import db

class MessageModel(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key = True)
    to_user = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)
    from_user = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)
    message = db.Column(db.String(512), nullable= False)
    status = db.Column(db.Integer)
    is_read = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    