import numpy as np

data = np.array([1, 2, 3, 4, 5])

print("first 2 ele: ", data[:2])
print("last 2 ele: ", data[3:])
print("sum: ", np.sum(data))
print("mean: ", np.mean(data))
print("standard deviation: ", np.std(data))
print("reverse: ", data[::-1])