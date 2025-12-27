from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.models import MedicationLog, UserMedication


def adherence_features(db: Session, user_med: UserMedication):
    last_7_days = datetime.utcnow() - timedelta(days=7)

    logs = (
        db.query(MedicationLog)
        .filter(MedicationLog.user_medication_id == user_med.id)
        .filter(MedicationLog.logged_at >= last_7_days)
        .all()
    )

    if not logs:
        return {
            "taken": 0,
            "missed": 0,
            "adherence_rate": 0.0
        }

    taken = sum(1 for l in logs if l.taken)
    missed = sum(1 for l in logs if not l.taken)
    total = taken + missed

    return {
        "taken": taken,
        "missed": missed,
        "adherence_rate": round(taken / total, 2) if total else 0.0
    }
