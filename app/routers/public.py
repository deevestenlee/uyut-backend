from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.seed import seed_data  # или ваша функция сидинга

router = APIRouter(tags=["Public"])

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/seed-db-secret-key")
def run_seed(db: Session = Depends(get_db)):
    try:
        seed_data(db)
        return {"message": "База данных успешно заполнена!"}
    except Exception as e:
        return {"error": str(e)}
