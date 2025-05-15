from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.auth import get_db, get_current_active_user, get_admin_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_book = crud.get_book(db, book.id)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db, book)

@router.get("/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.get_books(db)

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int, 
    book: schemas.BookCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)  # Only admins can update books
):
    updated_book = crud.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}")
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)  # Only admins can delete books
):
    result = crud.delete_book(db, book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} deleted"}