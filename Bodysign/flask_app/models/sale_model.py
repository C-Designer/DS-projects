from flask_app import db

class Sale(db.Model):
    __tablename__ = "sale"

    id = db.Column(db.Integer(), primary_key=True)
    is_sale = db.Column(db.Integer(), nullable=False)
    member_id = db.Column(db.Integer(), db.ForeignKey('member.id'), nullable=False)
    trainer_name = db.Column(db.String(), db.ForeignKey('trainer.name'), nullable=False)

    member = db.relationship('Member', backref='sale')
    trainer = db.relationship('Trainer', backref='sale')

    def __repr__(self):
        return f"{self.id}"