from fastapi import FastAPI
from octopus_exercise.api.routes import router

app = FastAPI()
app.include_router(router)

