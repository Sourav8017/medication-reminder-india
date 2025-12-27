from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.models import ReminderSchedule, MedicationLog, UserMedication


def generate_daily_schedules(
    db: Session,
    user_med: UserMedication,
    start_time: datetime | None = None
):
    """
    Create today's reminder times based on frequency_per_day.
    """
    start_time = start_time or datetime.utcnow().replace(hour=8, minute=0, second=0, microsecond=0)

    interval_hours = 24 // max(1, user_med.frequency_per_day)

    for i in range(user_med.frequency_per_day):
        t = start_time + timedelta(hours=i * interval_hours)
        sched = ReminderSchedule(
            user_medication_id=user_med.id,
            scheduled_time=t
        )
        db.add(sched)

    db.commit()


def mark_missed_doses(db: Session, now: datetime | None = None):
    """
    Any schedule older than 1 hour without a log is marked missed.
    """
    now = now or datetime.utcnow()
    cutoff = now - timedelta(hours=1)

    schedules = (
        db.query(ReminderSchedule)
        .filter(ReminderSchedule.active == True)
        .filter(ReminderSchedule.scheduled_time <= cutoff)
        .all()
    )

    for s in schedules:
        # check if a log exists
        exists = (
            db.query(MedicationLog)
            .filter(MedicationLog.user_medication_id == s.user_medication_id)
            .filter(MedicationLog.scheduled_time == s.scheduled_time)
            .first()
        )
        if not exists:
            db.add(MedicationLog(
                user_medication_id=s.user_medication_id,
                scheduled_time=s.scheduled_time,
                taken=False
            ))
        s.active = False

    db.commit()
