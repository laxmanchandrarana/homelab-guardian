from guardian.database import SessionLocal
from guardian.models.audit import Audit


class AuditRepository:

    def create(self, **kwargs):
        db = SessionLocal()
        obj = Audit(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        db.close()
        return obj

    def list(self):
        db = SessionLocal()
        rows = db.query(Audit).order_by(Audit.id.desc()).all()
        db.close()
        return rows
