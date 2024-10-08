from flask import Flask, request
from sqlalchemy import insert

from models import User, Photo, session, engine, Base

app = Flask(__name__)

@app.before_request
def before_request_func():
"""
Данная функция создает, привязывает базу данных.
"""
  Base.metadata.create_all(engine)

@app.route('/', methods=['GET'])
def all_photo():
"""
Эндпонит позволяет просмотреть все фото сохраненныне в базе
"""
  photos = session.query(Photo).all()
  photo_list = []
  for photo in photos:
    photo_list.append(photo.to_json())
  session.commit()
  return photo_list

@app.route('/upload', methods = ['POST'])
def upload_photo(photo_name: str):
"""
Эндпоинт сохраняет фото введенный пользователем в базу данных.
"""
  photo = request.form.get('photo_name', type = str)
  user = session.User.id
  new_photo = insert(Photo).values(name=photo, user_id = user.id))
  session.add(new_photo)
  session.commit()
  return "Фото успешно сохранен в базу"

@app.route('/download', methods = ['GET'])
def download_photo(idx: int):
"""
Эндпоинт позволяет скачать изоброжение.
"""
  photo = session.query(Photo).filter(id=idx).one()
  photo.fitchone()
  photo.save()
  return "Фото успешно сохранен."
        

if __name__ == '__main__':
  app.run()
