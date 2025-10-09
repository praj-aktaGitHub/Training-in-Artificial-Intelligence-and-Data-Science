from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Stud = [
    {'id': 1, 'name': 'Aaryan', 'department': 'AI', 'Marks': 91},
    {'id': 2, 'name': 'Prajakta', 'department': 'AI - ML', 'Marks': 96},
    {'id': 3, 'name': 'Rudra', 'department': 'AI-DS', 'Marks': 80},
    {'id': 4, 'name': 'Harsh', 'department': 'AI', 'Marks': 79},
    {'id': 5, 'name': 'Saamya', 'department': 'IT', 'Marks': 86},
]


@app.get("/students")
def get_all_students():
    return {"Students": Stud}