from mapmyworld.extensions import db, ma
from marshmallow_sqlalchemy import auto_field
from .users import User

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    register_status = db.Column(db.Boolean, nullable=False, server_default=db.text("1"))

    user = db.relationship('User')

    def __init__(self,  id=None, name=None, user_id=None, created_at=None, register_status=None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.created_at = created_at
        self.register_status = register_status


exclude = ("created_at","register_status")
class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        exclude = exclude

class CategorySerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        exclude = exclude
        load_instance = True
    id = auto_field()
    name = auto_field()