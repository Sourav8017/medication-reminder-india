from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.auth_dependency import get_current_user
from backend.database import get_db
from backend.models import User, UserMedication, ReminderSchedule, MedicationLog
from backend.reminder_utils import generate_daily_schedules, mark_missed_doses

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/generate/{user_medication_id}")
def generate_today(
    user_medication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    um = db.query(UserMedication).filter(UserMedication.id == user_medication_id).first()
    if not um or um.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Medication not found")

    generate_daily_schedules(db, um)
    return {"message": "Today's reminders generated"}


@router.get("/my")
def my_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mark_missed_doses(db)

    rows = (
        db.query(ReminderSchedule)
        .join(UserMedication)
        .filter(UserMedication.user_id == current_user.id)
        .all()
    )

    return [{
        "schedule_id": r.id,
        "medicine": r.user_medicine.medicine.name,
        "scheduled_time": r.scheduled_time,
        "active": r.active
    } for r in rows]


@router.post("/take/{schedule_id}")
def mark_taken(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sched = db.query(ReminderSchedule).filter(ReminderSchedule.id == schedule_id).first()
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")

    um = sched.user_medicine
    if um.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.add(MedicationLog(
        user_medication_id=um.id,
        scheduled_time=sched.scheduled_time,
        taken=True
    ))
    sched.active = False
    db.commit()

    return {"message": "Dose marked as taken"}
