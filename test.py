from rmq import start_mq, consumer, deliver
from threading import Thread

start_mq()

def get():
    for i in consumer.get():
        print("Consumer:", i)
       
Thread(target=get).start()

while True:
    deliver(input("Deliver: "))