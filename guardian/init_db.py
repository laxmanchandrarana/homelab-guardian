from guardian.database import Base
from guardian.database import engine

import guardian.models.audit
import guardian.models.backup
import guardian.models.restore
import guardian.models.incident

Base.metadata.create_all(bind=engine)

print("Guardian database initialized.")
