from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.utils.deps import get_db, get_current_user   # зависимости
from app.schemas.clinic import ClinicOut, ClinicUpdate  # схемы

router = APIRouter(prefix="/clinic", tags=["clinic"])


@router.get("/me", response_model=ClinicOut)
def get_clinic_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == current_user.clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Клиника не найдена")
    return clinic


@router.put("/me", response_model=ClinicOut)
def update_clinic_me(
    clinic_data: ClinicUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Разрешаем редактировать только суперадмину
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Нет прав для изменения данных клиники")

    clinic = db.query(models.Clinic).filter(models.Clinic.id == current_user.clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Клиника не найдена")

    for field, value in clinic_data.dict(exclude_unset=True).items():
        setattr(clinic, field, value)

    db.commit()
    db.refresh(clinic)
    return clinic
