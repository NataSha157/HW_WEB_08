from mongoengine import connect, Document, StringField, BooleanField, EmailField

import os
from dotenv import load_dotenv
load_dotenv()

db = os.getenv('MONGO_DB')
host = os.getenv('MONGO_URL')

connect(db=db,
        host=host)

class Contact(Document):
    fullname = StringField(max_length=150, required=True)
    e_mail = EmailField(max_length=40, required=True)
    send_mail = BooleanField(required=True, default=False)
    meta = {"collection":"contacts"}

