from app import create_applicaton, db
from app.models import *
from flask_migrate import Migrate

app = create_applicaton()
migrate = Migrate(app, db)

@app.shell_context_processor
def shell():
    return dict(
        db=db,
        Users=Users,
        Folowers=Folowers,
        Following=Following
    )

