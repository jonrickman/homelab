from models import user_factory
from app import app

user = user_factory.create_user(username="user", password="pass")
print(user)
with app.app_context():
    user.insert()
