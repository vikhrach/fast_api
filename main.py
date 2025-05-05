from fastapi import Body, FastAPI, Depends
from fastapi.params import Header
from pydantic import BaseModel
from enum import StrEnum
import badminton_model
import uvicorn

app = FastAPI()

def is_playable(weather:badminton_model.Weather):
    model = badminton_model.BadmintonModel("model/model.pkl")    
    return {"playability": model.predict(weather)}


@app.get("/sayhello")
def hello():
    return {"message": "Hello world"}

@app.post("/playability")
def playability(weather:badminton_model.Weather):
    playability = is_playable(weather)
    print(Body)
    return playability

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
