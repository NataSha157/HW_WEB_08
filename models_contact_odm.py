from mongoengine import connect, Document, StringField, BooleanField, EmailField

connect(db='hwWeb08',
        host='mongodb+srv://user231113:lo0depChcZ4ysyCJ@cluster0.hc2168m.mongodb.net/?retryWrites=true&w=majority')

class Contact(Document):
    fullname = StringField(max_length=150, required=True)
    e_mail = EmailField(max_length=40, required=True)
    send_mail = BooleanField(required=True, default=False)
    meta = {"collection":"contacts"}

