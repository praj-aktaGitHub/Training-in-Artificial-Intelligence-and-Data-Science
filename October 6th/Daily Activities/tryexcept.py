try:
    value = int(input("Enter a num:"))
    print(10 / value)
except ValueError:
    print("Invalid num, pl try again")
except ZeroDivisionError:
    print("Can't divide by zero")
finally:
    print("Execution slayed")