from fastapi import Depends, HTTPException, status
from app.models import user as user_model
from app.utils import deps

def require_role(required_role: str):
    def role_checker(current_user: user_model.User = Depends(deps.get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Доступ запрещён для роли {current_user.role}"
            )
        return current_user
    return role_checker
