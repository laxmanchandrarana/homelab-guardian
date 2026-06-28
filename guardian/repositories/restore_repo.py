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

    def add(self, restore):
        db = SessionLocal()
        db.add(restore)
        db.commit()
        db.refresh(restore)
        db.close()
        return restore

    def list(self):
        db = SessionLocal()
        rows = db.query(Restore).order_by(Restore.id.desc()).all()
        db.close()
        return rows

    def latest(self):
        db = SessionLocal()
        row = db.query(Restore).order_by(Restore.id.desc()).first()
        db.close()
        return row
