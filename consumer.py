import json
import os
import sys
import time

import pika

from models_contact_odm import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='HW_08_queue', durable=True)

    def callback(ch, method, body):
        message = json.loads(body.decode())
        print(f" [x] Received {message}")
        time.sleep(0.5)
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        a = Contact.objects(id=message['id']).first()
        if a.send_mail == False:
            a.update(send_mail = True)
            a.save()

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='HW_08_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)