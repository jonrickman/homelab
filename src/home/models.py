from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class Video(Base):
    __tablename__= "videos"

    id = Column(Integer, primary_key=True, index=True)
    title= Column(String)
    artist=Column(String)
    tags=Column(String)
    description=Column(String)
    
# from home.app import db, login_manager, app
# from flask_login import UserMixin
# from sqlalchemy.sql import func
# from sqlalchemy import DateTime, Column, String, Integer
# from werkzeug.security import generate_password_hash

# @login_manager.user_loader
# def load_user(user_id: int):
#     return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = Column(Integer, primary_key=True)
#     username = Column(String(20), unique=True, nullable=False)
#     password_hash = Column(String, nullable=False)
#     time_created = Column(DateTime(timezone=True), server_default=func.now())
#     time_updated = Column(DateTime(timezone=True), onupdate=func.now())

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

# class UserFactory:
#     def find_user(self, username:str) -> User:
#         users = User.query
#         return users.filter(User.username==username)

#     def get(self, user_id:str) -> User:
#         users = User.query
#         return users.filter(User.id==user_id)

#     def create_user(self, username: str, password: str) -> User:
#         password_hash = generate_password_hash(password)
#         kwargs = dict(username=username, password_hash=password_hash)
#         return User(**kwargs)

# class Video(db.Model):
#     id = Column(String, primary_key=True)
#     thumbnail = Column(String, nullable=True)




# user_factory = UserFactory()

# if __name__ == "__main__":

#     # Run this file directly to create the database tables.
#     print("Creating database tables...")
#     with app.app_context():
#         db.drop_all()
#         db.create_all()

#     print("Done!")
