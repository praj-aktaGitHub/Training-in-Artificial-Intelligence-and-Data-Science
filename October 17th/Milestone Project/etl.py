import pandas as pd

def process_visits():
    visits = pd.read_csv('data/visits.csv')
    doc = pd.read_csv('data/doctors.csv')
    patients = pd.read_csv('data/patients.csv')

    m1 = visits.merge(doc, on="DoctorID", how="left")
    m2 = m1.merge(patients, on="PatientID", how="left")

    m2["Month"] = pd.to_datetime(m2["Date"]).dt.month

    counts = m2["PatientID"].value_counts().to_dict()
    m2["Visits"] = m2["PatientID"].map(counts)

    m2["FollowUpRequired"] = m2["Visits"] > 1

    m2.to_csv("processed_visits.csv", index=False)
    return {"message": "processed_visits.csv created successfully!"}


