from typing import Iterable
from fastapi import Depends, HTTPException, status
from ..auth import get_current_user
from ..models import UserBase, RoleEnum


def require_roles(*roles: Iterable[RoleEnum]):
    def _checker(user: UserBase = Depends(get_current_user)) -> UserBase:
        if roles and user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
        return user
    return _checker
