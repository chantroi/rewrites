from rmq import start_mq, consumer, deliver

start_mq()

from threading import Thread

def get():
    for i in consumer.get():
        print("Consumer:", i)
       
Thread(target=get).start()

while True:
    deliver(input("Deliver: "))