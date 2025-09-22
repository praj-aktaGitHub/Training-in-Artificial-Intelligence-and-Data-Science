def multiplication(num):
    print(f"Multiplication table of {num}")
    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")

number = int(input("Enter a num:"))
result = multiplication(number)
print(result)





