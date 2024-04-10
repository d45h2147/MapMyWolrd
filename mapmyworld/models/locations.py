from mapmyworld.extensions import db, ma
from marshmallow import Schema, fields, validates, ValidationError
from .users import User

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    register_status = db.Column(db.Boolean, nullable=False, server_default=db.text("1"))

    user = db.relationship('User')

    def __init__(self, id=None, longitude=None, latitude=None, user_id=None, created_at=None, register_status=None):
        self.id = id
        self.longitude = longitude
        self.latitude = latitude
        self.user_id = user_id
        self.created_at = created_at
        self.register_status = register_status

exclude = ("created_at","register_status")
class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        exclude = exclude

class LocationSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        exclude = exclude