from fastapi import FastAPI
from routers import users

app = FastAPI(title="My FastAPI Project")

# Подключаем маршруты (роутеры)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to My FastAPI Project"}
