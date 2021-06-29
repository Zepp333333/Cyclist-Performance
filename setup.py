#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from cycperf import db, create_app
from cycperf.models import User

app = create_app()
with app.app_context():
    db.create_all()
