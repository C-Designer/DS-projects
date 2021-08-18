from flask_app import db

class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer(), primary_key=True)
    sex = db.Column(db.Integer(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    
    real = db.Column(db.Integer(), nullable=False)
    roman = db.Column(db.Integer(), nullable=False)
    human = db.Column(db.Integer(), nullable=False)
    ideal = db.Column(db.Integer(), nullable=False)
    agent = db.Column(db.Integer(), nullable=False)

    relation = db.Column(db.Integer(), nullable=False)
    trust = db.Column(db.Integer(), nullable=False)
    manual = db.Column(db.Integer(), nullable=False)
    confidence = db.Column(db.Integer(), nullable=False)
    culture = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return f"id : {self.id}"