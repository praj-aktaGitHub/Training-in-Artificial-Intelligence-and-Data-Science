Employee = {
    "name": "Aryan",
    "age": 28,
    "city": "London",
}
print(Employee)
print(Employee.get("city"))

Employee["email"] = "abc@gmail.com"
Employee["city"] = "Mumbai"
Employee.pop("city")
del Employee["age"]
print(Employee)