from db import db

class NotificationModel(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable= False)
    notification = db.Column(db.String(100), nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable= False)
    status = db.Column(db.Integer)
    is_sent = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    