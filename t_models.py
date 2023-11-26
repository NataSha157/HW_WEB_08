# Створення моделей для прямої загрузки в БД файлів .json (від викладача)
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(db='hwWeb08',
        host='mongodb+srv://user231113:lo0depChcZ4ysyCJ@cluster0.hc2168m.mongodb.net/?retryWrites=true&w=majority')


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