from mapmyworld.extensions import db, ma
from .users import User
from .locations import Location, LocationSchema
from .categories import Category, CategorySchema
from marshmallow import Schema, fields


class LocationCategoryReviewed(db.Model):
    __tablename__ = 'location_category_reviewed'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.ForeignKey('locations.id'), nullable=False)
    category_id = db.Column(db.ForeignKey('categories.id'), nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    reviewed_title = db.Column(db.Text, nullable=False)
    reviewed_desc = db.Column(db.Text, nullable=False)
    reviewed_star = db.Column(db.Integer, nullable=False, server_default=db.text("5"))
    reviewed_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    register_status = db.Column(db.Boolean, nullable=False, server_default=db.text("1"))

    category = db.relationship('Category')
    location = db.relationship('Location')
    user = db.relationship('User')

    def __init__(self,  id=None, location_id=None, category_id=None, user_id=None, reviewed_title=None, reviewed_desc=None, reviewed_star=None, reviewed_at=None, register_status=None):
        self.id = id
        self.location_id = location_id
        self.category_id = category_id
        self.user_id = user_id
        self.reviewed_title = reviewed_title
        self.reviewed_desc = reviewed_desc
        self.reviewed_star = reviewed_star
        self.reviewed_at = reviewed_at
        self.register_status = register_status


class LocationCategoryReviewedSchema(ma.SQLAlchemyAutoSchema):
    location = ma.Nested(LocationSchema)
    category = ma.Nested(CategorySchema)

    class Meta:
        model = LocationCategoryReviewed
        exclude = ("register_status",)
