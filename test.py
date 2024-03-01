from rmq import Consumer, Deliver
from threading import Thread

consumer = Consumer()
deliver = Deliver()
Thread(target=consumer.run).start()
Thread(target=deliver.run).start()

def get():
    for i in consumer.get():
        print("Consumer:", i)
       
Thread(target=get).start()

while True:
    deliver(input("Deliver: "))