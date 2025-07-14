from fastapi import FastAPI
from routes import bot

app = FastAPI()

app.include_router(bot.router, prefix="/bot")

@app.get("/")
def root():
    return {"message": "SmartFinanceBot API is running"}
