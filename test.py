from rmq import Consumer, Deliver
from threading import Thread

consumer = Consumer()
deliver = Deliver()
Thread(target=consumer.run).start()

deliver.send("Test")
deliver.send("hello")

for i in consumer.get():
    print(i)