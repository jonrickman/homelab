from home.models import user_factory
from home.app import app

user = user_factory.create_user(username="user", password="pass")
print(user)
with app.app_context():
    user.insert()
