from datetime import datetime

from mongoengine import connect, Document, StringField, ListField, ReferenceField, NULLIFY, DateField

connect(db='hwWeb08',
        host='mongodb+srv://user231113:lo0depChcZ4ysyCJ@cluster0.hc2168m.mongodb.net/?retryWrites=true&w=majority')

class Author(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = DateField() # Поле типу дата
    born_location = StringField(max_length=150)
    description = StringField(required=True)
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=30), required=True, default=list)
    author = ReferenceField('Author', reverse_delete_rule=NULLIFY)
    quote = StringField(required=True)
    meta = {"collection": "quotes"}


