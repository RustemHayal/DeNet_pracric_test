from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from typing import Dict, Any

engine = create_engine('sqlite:///photo_collection.db')

Session = sessionmaker(engine)
session = Session()

Base = declarative_base(bind=engine)

class User(Base):
"""
Класс пользователя. При подключении нового пользователя необходимо ввести следующие значения:
name - имя пользоваетля, surname-фамилию, email_adress -адрес электронной почты
"""
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  surname = Column(String, nullable=False)
  email = Column(String, nullable=False)
  
  @classmethod
      def get_user_by_email(cls, email: str):
          try:
              user = session.query(User).filter(User.email == email).one()
              return user
          except NoResultFound:
              print(f"Пользователь с {email} существует")
          except MultipleResultsFound:
              print("Ошибка уникальности индекса")

  def __repr__(self):
    return f'Пользователь {self.surname} {self.name}'

  def to_join(self) -> Dict[str, Any]:
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Photo(Base):
  __tablename__ = 'photos'

  id = Column(Integer, primary_key = True)
  name = Column(String, nullable = False)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relashionship("User", backref='photos')

  def __repr__(self):
    return f'Фото {self.name}'

  def to_join(self) -> Dict[str, Any]:
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
