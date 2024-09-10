from init import db, ma 


class User(db.Model):
    # Name of Table
    __tablename__= "Users"
    
    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,)
    email = db.Columns(db.String, nullable=False, unique=True)
    password = db.Columns(db.String, nullable=False)
    is_admin = db.Columns(db.Boolean, default=False)
    
class UserSchema(ma.Scheme):
    class Meta:
        fields=("id", "name", "email", "password", "is_admin")
        
# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
user_schema = UserSchema(many=True, exclude=["password"])