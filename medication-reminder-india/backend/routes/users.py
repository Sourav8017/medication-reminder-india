from fastapi import APIRouter, Depends

from backend.auth_dependency import get_current_user
from backend.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "age": current_user.age,
        "phone": current_user.phone,
        "created_at": current_user.created_at
    }
