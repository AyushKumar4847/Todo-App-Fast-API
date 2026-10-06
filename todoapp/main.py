from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers.auth import router as AuthRouter
from .routers.todos import router as TodoRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/")(lambda: "Hello World")
Base.metadata.create_all(bind=engine)
app.include_router(AuthRouter)
app.include_router(TodoRouter)

