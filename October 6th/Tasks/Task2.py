import yaml
import logging

Config1 = {
    "app": dict(name="Student Portal", version=1.0),
    "database":{
        "host": "localhost",
        "port": 3306,
        "user": "root"
    }
}

with open('Config1.yaml', 'w')as f:
    yaml.dump(Config1, f)
try:
    with open("Config1.yaml", "r") as f:
        data = yaml.safe_load(f)
        logging.info("Config1 loaded successfully")

        connection_string = f"Connecting to {data['database']['host']}:{data['database']['port']}"
        print(connection_string)

except FileNotFoundError:
    logging.error("Config1.yaml not found")
    print("Config1.yaml not found")

print(data)