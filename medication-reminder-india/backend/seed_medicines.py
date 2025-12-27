import pandas as pd

from backend.database import SessionLocal
from backend.models import Medicine

CSV_PATH = "backend/data/nlem_medicines.csv"


def seed_medicines():
    db = SessionLocal()

    existing = db.query(Medicine).first()
    if existing:
        print("Medicines already seeded.")
        db.close()
        return

    df = pd.read_csv(CSV_PATH)

    for _, row in df.iterrows():
        med = Medicine(
            name=row["medicine_name"],
            condition=row["condition"],
            medicine_type=row["medicine_type"],
            risk_if_missed=row["risk_if_missed"]
        )
        db.add(med)

    db.commit()
    db.close()
    print("Indian NLEM medicines seeded successfully.")


if __name__ == "__main__":
    seed_medicines()
