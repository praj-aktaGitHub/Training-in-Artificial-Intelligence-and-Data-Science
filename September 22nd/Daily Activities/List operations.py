def stats(num):
    total = sum(num)
    maximum = max(num)
    minimum = min(num)
    length = len(num)
    avg = total / length
    return total, maximum, minimum, avg, length

nums = [10, 20, 30, 40, 50]
print(stats(nums))
