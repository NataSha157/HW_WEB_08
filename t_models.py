# Створення моделей для прямої загрузки в БД файлів .json (від викладача)
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

import os
from dotenv import load_dotenv
load_dotenv()

db = os.getenv('MONGO_DB')
host = os.getenv('MONGO_URL')

connect(db=db,
        host=host)


class Author1(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50) # Поле строкове, а не дата
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors1"}


class Quote1(Document):
    author = ReferenceField(Author1, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes1"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)