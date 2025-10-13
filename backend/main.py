from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Dates(BaseModel):
    start_date: str
    end_date: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/date")
def date(dates: Dates):
    result = f"From Server: {dates.start_date} ~ {dates.end_date}"
    return {"result": result}

