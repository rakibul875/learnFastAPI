from fastapi import FastAPI
app= FastAPI()

@app.get("/")
def view():
    return {"message": "Hello, World!"}