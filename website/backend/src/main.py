from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.users import router as router_users
from src.routers.performers import router as router_performers
from src.routers.albums import router as router_albums
from src.routers.genres import router as router_genres
from src.routers.tracks import router as router_tracks
from src.routers.moodtags import router as router_moodtags
from src.routers.actiontags import router as router_actiontags
from src.routers.playlists import router as router_playlists

import src.models.create_models

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены, для продакшена указывайте конкретные
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(router_users)
app.include_router(router_performers)
app.include_router(router_albums)
app.include_router(router_genres)
app.include_router(router_tracks)
app.include_router(router_moodtags)
app.include_router(router_actiontags)
app.include_router(router_playlists)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)