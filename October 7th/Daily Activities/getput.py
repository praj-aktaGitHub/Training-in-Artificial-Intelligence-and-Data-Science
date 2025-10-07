from fastapi import FastAPI

app = FastAPI()

@app.get("/students")
def get_student():
    return {"GET req"}

@app.post("/students")
def create_student():
    return {"POST req"}

@app.put("/students")
def update_student():
    return {"PUT req"}

@app.delete("/students")
def del_student():
    return {"DELETE req"}