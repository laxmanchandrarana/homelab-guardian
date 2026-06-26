from guardian.database import SessionLocal
from guardian.models.backup import Backup


class BackupRepository:

    def all(self):

        db = SessionLocal()

        try:
            return db.query(Backup).all()
        finally:
            db.close()

    def add(self, backup):

        db = SessionLocal()

        db.add(backup)

        db.commit()

        db.refresh(backup)

        db.close()

        return backup

    def create(self, **kwargs):
        db = SessionLocal()
        obj = Backup(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        db.close()
        return obj

    def list(self):
        db = SessionLocal()
        rows = db.query(Backup).order_by(Backup.id.desc()).all()
        db.close()
        return rows

    def latest(self):
        db = SessionLocal()
        row = db.query(Backup).order_by(Backup.id.desc()).first()
        db.close()
        return row
