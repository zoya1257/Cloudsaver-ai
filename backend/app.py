from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CloudSaver-AI backend is running successfully!"}
