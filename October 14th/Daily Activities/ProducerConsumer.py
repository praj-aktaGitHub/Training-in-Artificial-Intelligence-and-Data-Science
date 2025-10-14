import threading
import queue
import time
 
q = queue.Queue()
 
 
def producer():
    for i in range(5):
        print(f"producing {i}")
        q.put(i)
        time.sleep(1)
    print("producer done")
 
 
def consumer():
    while True:
        item = q.get()
        print(f"consumed {item}")
        q.task_done()
 
 
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer, daemon=True)
 
producer_thread.start()
consumer_thread.start()
 
producer_thread.join() 
q.join() 
print("All tasks done")
