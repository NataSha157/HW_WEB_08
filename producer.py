import json

from faker import Faker
from datetime import datetime

import pika

from models_contact_odm import Contact

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW_08 exchange', exchange_type='direct')
channel.queue_declare(queue='HW_08_queue', durable=True)
channel.queue_bind(exchange='HW_08 exchange', queue='HW_08_queue')


def create_users(numbers=1):
    for i in range(numbers):
        user = Contact(fullname=fake.name(), e_mail=fake.email(), send_mail=False)
        user.save()


def get_id():
    data = Contact.objects().all()
    res = []
    for i in data:
        res.append(i.id)
    return res


def create_tasks():
    for i in get_id():
        message = {
            'id': str(i),
            'payload': f"Date: {datetime.now().isoformat()}. Contact id: {i}"
        }
        channel.basic_publish(exchange='HW_08 exchange', routing_key='HW_08_queue', body=json.dumps(message).encode())

    connection.close()


if __name__ == '__main__':
    create_users(10)
    create_tasks()
