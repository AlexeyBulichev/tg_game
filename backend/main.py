from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from auth import check_telegram_auth

app = FastAPI()

# Разрешим запросы от твоего WebApp
origins = [
    "https://tg-game-webapp.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/")
async def auth(init_data: str = Form(...)):
    user_data = check_telegram_auth(init_data)
    if not user_data:
        return {"ok": False, "reason": "invalid hash"}
    return {"ok": True, "user": user_data}
