import pika
import pandas as pd
import json

def send_visits_to_queue():
    visits_df = pd.read_csv("data/visits.csv")

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="visit_queue")

    for _, row in visits_df.iterrows():
        visit_csv = ",".join(str(x) for x in row.values)
        channel.basic_publish(exchange="", routing_key="visit_queue", body=visit_csv)
        print(f"[Producer] Sent VisitID: {row['VisitID']}")

    connection.close()


send_visits_to_queue()

