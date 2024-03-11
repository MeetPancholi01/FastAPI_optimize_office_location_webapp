from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router
app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5501"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
