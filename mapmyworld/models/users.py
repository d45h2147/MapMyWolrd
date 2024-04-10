from mapmyworld.extensions import db, ma

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, server_default=db.text("0"))
    created_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    register_status = db.Column(db.Boolean, nullable=False, server_default=db.text("1"))


    def __init__(self, user_id=None, first_name=None, last_name=None, is_admin=None, created_at=None, register_status=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.created_at = created_at
        self.register_status = register_status

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User