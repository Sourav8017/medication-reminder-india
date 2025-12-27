from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth_dependency import get_current_user
from backend.database import get_db
from backend.models import Medicine, UserMedication, User

router = APIRouter(prefix="/medications", tags=["Medications"])


@router.post("/add")
def add_medication(
    medicine_id: int,
    dosage: str,
    frequency_per_day: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check medicine exists
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Add medication for user
    user_med = UserMedication(
        user_id=current_user.id,
        medicine_id=medicine_id,
        dosage=dosage,
        frequency_per_day=frequency_per_day
    )

    db.add(user_med)
    db.commit()
    db.refresh(user_med)

    return {
        "message": "Medication added successfully",
        "user_medication_id": user_med.id
    }


@router.get("/my")
def get_my_medications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meds = (
        db.query(UserMedication)
        .filter(UserMedication.user_id == current_user.id)
        .all()
    )

    return [
        {
            "user_medication_id": m.id,
            "medicine_name": m.medicine.name,
            "condition": m.medicine.condition,
            "dosage": m.dosage,
            "frequency_per_day": m.frequency_per_day,
            "risk_if_missed": m.medicine.risk_if_missed
        }
        for m in meds
    ]
