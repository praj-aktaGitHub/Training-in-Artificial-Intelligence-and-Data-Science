import sys
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
sys.path.append(os.path.dirname(__file__))
from etl import process_visits
from fastapi import FastAPI, HTTPException,Request
from analytics import generateKPI_report

from patients import router as patients_router
from doctors import router as doctors_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(patients_router, prefix="/patients", tags=["Patients"])
app.include_router(doctors_router, prefix="/doctors", tags=["Doctors"])

@app.get("/")
def read_root():
    return FileResponse("static/dashboard.html")

@app.get("/process-visits")
def run_visit_processing():
    return process_visits()

@app.get("/generate-kpi")
def run_kpi_report():
    return generateKPI_report()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Healthcare API"}

