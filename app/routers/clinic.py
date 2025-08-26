from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.schemas.clinic import ClinicOut, ClinicUpdate
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/clinic", tags=["clinic"])

@router.get("/me", response_model=ClinicOut)
def get_clinic_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Получение данных клиники для текущего пользователя.
    - superadmin: возвращает первую клинику
    - admin/registrar/doctor: возвращает клинику по clinic_id
    """
    if current_user.role.lower() == "superadmin":
        clinic = db.query(models.ClinicProfile).first()
        if not clinic:
            raise HTTPException(status_code=404, detail="Клиника не найдена")
    else:
        if not current_user.clinic_id:
            raise HTTPException(
                status_code=400,
                detail="У пользователя не привязана клиника. Свяжите его с clinic_id"
            )
        clinic = db.query(models.ClinicProfile).filter(
            models.ClinicProfile.id == current_user.clinic_id
        ).first()
        if not clinic:
            raise HTTPException(status_code=404, detail="Клиника не найдена")

    return clinic


@router.put("/me", response_model=ClinicOut)
def update_clinic_me(
    clinic_data: ClinicUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Редактирование данных клиники
    - Только admin и superadmin могут изменять
    """
    if current_user.role.lower() not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Нет прав для изменения данных клиники")

    # Определяем клинику
    if current_user.role.lower() == "superadmin":
        clinic = db.query(models.ClinicProfile).first()
    else:
        if not current_user.clinic_id:
            raise HTTPException(status_code=400, detail="У пользователя нет привязанной клиники")
        clinic = db.query(models.ClinicProfile).filter(
            models.ClinicProfile.id == current_user.clinic_id
        ).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Клиника не найдена")

    # Обновляем только переданные поля
    for field, value in clinic_data.dict(exclude_unset=True).items():
        setattr(clinic, field, value)

    db.commit()
    db.refresh(clinic)
    return clinic
