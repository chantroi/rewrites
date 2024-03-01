from rmq import Consumer, Deliver
from threading import Thread

consumer = Consumer()
deliver = Deliver()
Thread(target=consumer.run).start()

while True:
    text = input("CMD:")
    if text.startswith("c:"):
        print(next(consumer.get()))
    else:
        deliver.send(text)