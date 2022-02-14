import json
import pika
import settings
import time

def consum(): 
    k = 0  
    credential = pika.PlainCredentials(settings.credentialname, settings.credentialpass)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.rabbitmqhost,credentials=credential))
    channel = connection.channel()
    data = []
    # Get ten messages and break out
    for method_frame, properties, body in channel.consume(queue=settings.queue,auto_ack=False):

        # Display the message parts
        # print(method_frame)
        # print(properties)
        # print(body)
        msg = json.loads(body)
        print(msg)
        data.append(msg)

        # Acknowledge the message
        # channel.basic_ack(method_frame.delivery_tag,multiple=False)

        # Escape out of the loop after 10 messages
        if method_frame.delivery_tag == 1:
            break

    # Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    # print('Requeued %i messages' % requeued_messages)

    # Close the channel and the connection

    channel.close()
    connection.close()
    return data