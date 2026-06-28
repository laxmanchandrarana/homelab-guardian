from guardian.database import SessionLocal
from guardian.models.incident import Incident


class IncidentRepository:

    def create(self, **kwargs):
        db = SessionLocal()
        obj = Incident(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        db.close()
        return obj

    def list(self):
        db = SessionLocal()
        rows = db.query(Incident).order_by(Incident.id.desc()).all()
        db.close()
        return rows

    def add(self, incident):
        db = SessionLocal()
        db.add(incident)
        db.commit()
        db.refresh(incident)
        db.close()
        return incident

    def latest(self):
        db = SessionLocal()
        row = db.query(Incident).order_by(Incident.id.desc()).first()
        db.close()
        return row
