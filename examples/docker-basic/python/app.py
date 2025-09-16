import numpy as np
import time

print("Hello from inside the Docker container!")

for i in range(3):
    print(f"Counting: {i+1}")
    time.sleep(1)

print("Goodbye!")

print("Numpy array example:", np.array([1, 2, 3]))
