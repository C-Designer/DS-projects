from flask_app import db

class Machine(db.Model):
    __tablename__ = "machine"

    id = db.Column(db.Integer(), primary_key=True)
    q1 = db.Column(db.Float(), nullable=False)
    q2 = db.Column(db.Float(), nullable=False)
    q3 = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"q1 : {self.q1} q2 : {self.q2} q3 : {self.q3}"