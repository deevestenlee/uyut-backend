from fastapi import APIRouter

router = APIRouter(tags=["Admin"])

@router.get("/status")
def admin_status():
    return {"status": "admin active"}
