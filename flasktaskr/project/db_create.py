from views import db
from models import Task
from datetime import date

db.create_all()

db.session.add(Task("part 2 tutorial 끝내기", date(2017, 10, 1), 1, 1))
db.session.add(Task("Real Python 끝내기", date(2017, 12, 20), 10, 1))

db.session.commit()