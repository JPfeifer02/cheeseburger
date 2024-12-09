import threading
import random
import time

class ControlledProducer:
    def __init__(self, total_burgers):
        # Buffers and synchronization primitives
        self.buffer_milk = [0] * 9
        self.buffer_cheese = [0] * 4
        self.milk_lock = threading.Lock()
        self.cheese_lock = threading.Lock()
        self.milk_semaphore = threading.Semaphore(9)
        self.milk_used_semaphore = threading.Semaphore(0)
        self.cheese_semaphore = threading.Semaphore(0)
        
        self.total_burgers = total_burgers
        self.burgers_created = 0
        self.burgers_lock = threading.Lock()
        self.stop_event = threading.Event()
        
        self.milk_index = 0
        self.cheese_index = 0

    def milk_producer(self, producer_id):
        while not self.stop_event.is_set():
            milk_needed = self.milk_semaphore.acquire(blocking=False)
            if not milk_needed:
                if self.stop_event.is_set():
                    break
                time.sleep(0.1)
                continue
            
            with self.milk_lock:
                while self.buffer_milk[self.milk_index] != 0:
                    self.milk_lock.release()
                    time.sleep(0.1)
                    self.milk_lock.acquire()
                self.buffer_milk[self.milk_index] = producer_id
                print(f"Milk Producer {producer_id}: Produced milk at index {self.milk_index}")
                self.milk_index = (self.milk_index + 1) % 9
            self.milk_used_semaphore.release()

    def cheese_producer(self, producer_id):
        while not self.stop_event.is_set():
            # Wait for 3 milk bottles
            try:
                self.milk_used_semaphore.acquire(timeout=1)
                self.milk_used_semaphore.acquire(timeout=1)
                self.milk_used_semaphore.acquire(timeout=1)
            except threading.Semaphore.TimeoutError:
                if self.stop_event.is_set():
                    break
                continue
            
            with self.milk_lock:
                milk_ids = []
                for _ in range(3):
                    for i in range(len(self.buffer_milk)):
                        if self.buffer_milk[i] != 0:
                            milk_ids.append(self.buffer_milk[i])
                            self.buffer_milk[i] = 0
                            self.milk_semaphore.release()
                            break
            
            cheese_id = int(f"{producer_id}{''.join(map(str, milk_ids))}")
            
            with self.cheese_lock:
                while self.buffer_cheese[self.cheese_index] != 0:
                    self.cheese_lock.release()
                    time.sleep(0.1)
                    self.cheese_lock.acquire()
                self.buffer_cheese[self.cheese_index] = cheese_id
                print(f"Cheese Producer {producer_id}: Produced cheese {cheese_id} at index {self.cheese_index}")
                self.cheese_index = (self.cheese_index + 1) % 4
            self.cheese_semaphore.release()

    def cheeseburger_producer(self):
        while True:
            # Wait for 2 cheese slices
            self.cheese_semaphore.acquire()
            self.cheese_semaphore.acquire()
            
            with self.cheese_lock:
                cheese_ids = []
                for _ in range(2):
                    for i in range(len(self.buffer_cheese)):
                        if self.buffer_cheese[i] != 0:
                            cheese_ids.append(self.buffer_cheese[i])
                            self.buffer_cheese[i] = 0
                            break
            
            cheeseburger_id = ''.join(map(str, cheese_ids))
            
            with self.burgers_lock:
                self.burgers_created += 1
                print(f"Cheeseburger Producer: Created Cheeseburger with ID {cheeseburger_id}")
                
                if self.burgers_created >= self.total_burgers:
                    self.stop_event.set()
                    break

    def run(self):
        # Create the threads
        milk_threads = [threading.Thread(target=self.milk_producer, args=(i + 1,)) for i in range(3)]
        cheese_threads = [threading.Thread(target=self.cheese_producer, args=(i + 4,)) for i in range(2)]
        cheeseburger_thread = threading.Thread(target=self.cheeseburger_producer)

        # Start threads
        for t in milk_threads:
            t.daemon = True
            t.start()
        for t in cheese_threads:
            t.daemon = True
            t.start()
        cheeseburger_thread.start()

        # Wait for cheeseburger thread to finish
        cheeseburger_thread.join()

def main():
    num_burgers = int(input("How many burgers do you want? "))
    producer = ControlledProducer(num_burgers)
    producer.run()

if __name__ == "__main__":
    main()
