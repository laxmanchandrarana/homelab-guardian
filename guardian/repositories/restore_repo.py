from guardian.database import SessionLocal
from guardian.models.restore import Restore


class RestoreRepository:

    def create(self, **kwargs):
        db = SessionLocal()
        obj = Restore(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        db.close()
        return obj

    def list(self):
        db = SessionLocal()
        rows = db.query(Restore).order_by(Restore.id.desc()).all()
        db.close()
        return rows

