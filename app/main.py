from fastapi import FastAPI
from app.database import Base, engine
from app.routers import books, customers
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")

# Include authentication router
app.include_router(auth_router)

# Include other routers
app.include_router(books.router)
app.include_router(customers.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore API"}