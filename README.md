# Concurrent Milk, Cheese, and Cheeseburger Production Simulator
## Overview
A Python multithreading program that simulates a producer-consumer scenario with synchronized milk, cheese, and cheeseburger production. The program demonstrates complex thread synchronization using semaphores, locks, and controlled production.

![Console output](https://imgur.com/a/dYt37wT)

## Features
- Concurrent milk production by multiple producers
- Cheese production using 3 milk bottles per slice
- Cheeseburger creation from 2 cheese slices
- Thread-safe buffer management
- Precise production control based on user-specified burger count

## Requirements
- Python 3.x
- Threading module
- Standard Python libraries

## How to Run the Program
### Step 1: Setup
Ensure you have Python 3 installed on your system.

### Step 2: Running the Program
Execute the script from the terminal:
```bash
python3 milk_cheese_burger_producer.py
```

### Step 3: Using the Program
When prompted, enter the number of cheeseburgers you want to produce:
```
How many burgers do you want? 3
```
The program will then:
- Produce milk
- Create cheese slices
- Manufacture cheeseburgers
- Stop when the specified number of burgers is created

### Step 4: Observing Production
Watch real-time output showing:
- Milk production details
- Cheese slice creation
- Cheeseburger manufacturing

## Synchronization Mechanics
- Milk producers use a semaphore to manage buffer space
- Cheese producers require 3 milk bottles per slice
- Cheeseburger production needs 2 cheese slices
- Locks prevent race conditions in shared buffers

## Limitations
- Fixed number of milk and cheese producers
- Simplified production model
- Demonstration of synchronization concepts

## Future Improvements
- Dynamic producer count
- More complex production rules
- Enhanced error handling
- Configurable buffer sizes
