from mongoengine import connect, Document, StringField, ListField, ReferenceField, NULLIFY, DateField

import os
from dotenv import load_dotenv
load_dotenv()

db = os.getenv('MONGO_DB')
host = os.getenv('MONGO_URL')

connect(db=db, host=host)

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


