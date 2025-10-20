import pandas as pd
def generateKPI_report():
    # load data
    processed_visits = pd.read_csv("processed_visits.csv")
    processed_visits["Cost"] = processed_visits["Cost"].astype(float)
    processed_visits["Date"] = pd.to_datetime(processed_visits["Date"])


    # avg cost per visit per p
    avg_cost_per_patient = (
        processed_visits.groupby(["PatientID", "Name_y"])["Cost"]
        .mean()
        .reset_index()
        .rename(columns={"Cost": "AvgCostPerVisit"})
    )

    # most visited doc
    doc_visits = processed_visits["DoctorID"].value_counts().reset_index()
    doc_visits.columns = ["DoctorID", "VisitCount"]
    doctor_details = processed_visits[["DoctorID", "Name_x", "Specialization"]].drop_duplicates()
    most_visited = doc_visits.merge(doctor_details, on="DoctorID", how="left")
    top_doc = most_visited.iloc[0]

    # no of visits per p
    visit_counts = processed_visits["PatientID"].value_counts().reset_index()
    visit_counts.columns = ["PatientID", "VisitCount"]

    # monthly revenue
    processed_visits["Month"] = processed_visits["Date"].dt.to_period("M")
    monthly_revenue = (
        processed_visits.groupby("Month")["Cost"]
        .sum()
        .reset_index()
        .rename(columns={"Cost": "MonthlyRevenue"})
    )

    # save all to kpi_report.txt
    with open("kpi_report.txt", "w", encoding="utf-8") as f:
        f.write("   KPI Report   \n\n")

        f.write("Most visited doc:\n")
        f.write(f"Name: {top_doc['Name_x']}\n")
        f.write(f"Specialization: {top_doc['Specialization']}\n")
        f.write(f"Visit Count: {top_doc['VisitCount']}\n\n")

        f.write("Avg cost per visit per patient:\n")
        for _, row in avg_cost_per_patient.iterrows():
            f.write(f"{row['Name_y']} ({row['PatientID']}): {row['AvgCostPerVisit']:.2f}\n")
        f.write("\n")

        f.write("No. of visits per patient:\n")
        for _, row in visit_counts.iterrows():
            f.write(f"{row['PatientID']}: {row['VisitCount']} visits\n")
        f.write("\n")

        f.write("Monthly Revenue:\n")
        for _, row in monthly_revenue.iterrows():
            f.write(f"{row['Month']}: ₹{row['MonthlyRevenue']:.2f}\n")

    with open("kpi_report.txt", "r", encoding="utf-8") as f:
        report_text = f.read()

    return {"message": "KPI report generated successfully!", "report": report_text}
