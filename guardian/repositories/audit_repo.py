from guardian.database import SessionLocal
from guardian.models.audit import Audit


class AuditRepository:

    def add(self, audit):
        db = SessionLocal()
        db.add(audit)
        db.commit()
        db.refresh(audit)
        db.close()
        return audit

    def list(self):
        db = SessionLocal()
        rows = db.query(Audit).order_by(Audit.id.desc()).all()
        db.close()
        return rows
