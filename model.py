from extions import db
class dbModel(db.Model):
    __tablename__ = "Sign_in"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    status = db.Column(db.String(10), nullable = False)
    note = db.Column(db.String(1000), nullable = True)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)