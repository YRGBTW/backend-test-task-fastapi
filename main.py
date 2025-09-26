from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import categories, posts, users, admin, auth

app = FastAPI()


api_prefix = "/api/v1"
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


app.include_router(auth.router, prefix= api_prefix)
app.include_router(users.router, prefix= api_prefix)
app.include_router(posts.router, prefix= api_prefix)
app.include_router(categories.router, prefix= api_prefix)
app.include_router(admin.router, prefix= api_prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)