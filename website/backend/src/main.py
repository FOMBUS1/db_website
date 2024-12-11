from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.users import router as router_users
from src.routers.performers import router as router_performers


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы со всех доменов (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(router_users)
app.include_router(router_performers)