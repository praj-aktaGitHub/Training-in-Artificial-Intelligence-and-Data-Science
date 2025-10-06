import csv
import logging

logging.basicConfig(filename='sales.log',level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    with open('sales.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                price = int(row['price'])
                quantity = int(row['quantity'])
                total = price * quantity
                print(f"{row['product']},{row['price']},{row['quantity']},{total}")
                logging.info(f"{row['product']} total_sale = {total}")
            except ValueError:
                logging.error(f"Invalid numeric value")
except FileNotFoundError:
    logging.error("sales.csv not found")
    print("sales.csv Missing file")
