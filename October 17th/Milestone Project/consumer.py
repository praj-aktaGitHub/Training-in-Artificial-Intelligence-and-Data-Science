import pika
import pandas as pd
import time
from io import StringIO
import logging



logging.basicConfig(
    filename="queueLog.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

def process_visit(ch, method, properties, body):
    start = time.time()
    try:
        from io import StringIO

        csv_line = body.decode().strip()
        fields = csv_line.split(",")

        if len(fields) != 5:
            raise ValueError(f"Expected 5 fields, got {len(fields)}: {fields}")

        visit_record = pd.DataFrame([fields], columns=["VisitID", "PatientID", "DoctorID", "Date", "Cost"])




        # load data
        visits = visit_record
        doc = pd.read_csv('data/doctors.csv')
        patients = pd.read_csv('data/patients.csv')
        processed_visits = pd.read_csv('processed_visits.csv')


        # merge
        m1 = visits.merge(doc, on="DoctorID", how="left")
        m2 = m1.merge(patients, on="PatientID", how="left")

        # cal new cols
        m2["Month"] = pd.to_datetime(m2["Date"]).dt.month
        m2["Visits"] = 1
        m2["FollowUpRequired"] = False

        # save report
        m2.to_csv(f"GeneratedReports/report_{m2['VisitID'].values[0]}.csv", index=False)
        print(f"[Consumer] Processed {m2['VisitID'].values[0]} in {round(time.time() - start, 2)}s ")
        logging.info(f"[Consumer] Processed {m2['VisitID'].values[0]} in {round(time.time() - start, 2)}s ")
        with open("queueLog.log", "a") as log:
            log.write(f"{m2['VisitID']},SUCCESS,{round(time.time() - start, 2)}s,{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            # follow up
            visit_id = m2["VisitID"].values[0]  # Get VisitID from m2
            rec = processed_visits[processed_visits["VisitID"] == visit_id]  # Locate matching row

            if not rec.empty and rec["FollowUpRequired"].values[0]:
                with open("queueLog.log", "a") as log:
                    log.write(f"{visit_id},FOLLOWUP_REQUIRED,{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

            #missing id
            visit_id = visit_record["VisitID"].values[0]

            # doc id
            if pd.isna(visit_record["DoctorID"].values[0]) or visit_record["DoctorID"].values[0] == "":
                with open("queueLog.log", "a") as log:
                    log.write(f"{visit_id},ERROR,MISSING_DOCTORID,{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # patient id
            if pd.isna(visit_record["PatientID"].values[0]) or visit_record["PatientID"].values[0] == "":
                with open("queueLog.log", "a") as log:
                    log.write(f"{visit_id},ERROR,MISSING_PATIENTID,{time.strftime('%Y-%m-%d %H:%M:%S')}\n")


    except Exception as e:
        print(f"[Consumer] Failed Error: {e}")
        logging.info(f"[Consumer] Failed Error: {e}")
        with open("queueLog.log", "a") as log:
            log.write(f"UNKNOWN_ID,FAILURE,0s,{time.strftime('%Y-%m-%d %H:%M:%S')},{str(e)}\n")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="visit_queue")
    channel.basic_consume(queue="visit_queue", on_message_callback=process_visit, auto_ack=True)
    print("Consumer started. Waiting for messages...")
    channel.start_consuming()

start_consumer()
