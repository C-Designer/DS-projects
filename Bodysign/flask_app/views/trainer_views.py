from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask_app.models.trainer_model import Trainer
from flask_app.models.sale_model import Sale
from flask_app import db

bp = Blueprint('trainer', __name__)

@bp.route('/trainer/', methods=['POST'])
def add_trainer():

    if request.method == "POST":

        try:
            name = str(request.form['name'])
            sex = int(request.form['sex'])
            age = int(request.form['age'])

            real = int(request.form['real'])
            roman = int(request.form['roman'])
            human = int(request.form['human'])
            ideal = int(request.form['ideal'])
            agent = int(request.form['agent'])
            
            relation = int(request.form['relation'])
            trust = int(request.form['trust'])
            manual = int(request.form['manual'])
            confidence = int(request.form['confidence'])
            culture = int(request.form['culture'])
        except:
            return "모든 값을 올바르게 기입하여 주세요.  <a href='/trainer'>돌아가기</a>", 400

        trainer = Trainer(name=name, sex=sex, age=age, real=real, roman=roman, human=human, ideal=ideal, agent=agent, relation=relation, trust=trust, manual=manual, confidence=confidence, culture=culture)
        raw_trainer = Trainer.query.filter(Trainer.name == name).first()
        sales = None
        # id를 확인하여 이미 있는 회원인지 확인
        if raw_trainer:
            sales = Sale.query.filter(Sale.trainer_name == raw_trainer.name).all()
            delete_trainer(raw_trainer.name)
            
        db.session.add(trainer)
        if sales:
            for s in sales:
                sale = Sale(id=s.id, is_sale=s.is_sale, member_id=s.member_id, trainer_name=s.trainer_name)
                db.session.add(sale)

        db.session.commit()
        return redirect(url_for('main.trainer_index'), code=200)

@bp.route('/trainer/', defaults={ 'trainer_name' : None })
@bp.route('/trainer/<trainer_name>')
def delete_trainer(trainer_name):
    # 던진 값이 없을시 404 반환
    if not trainer_name:
        return "반환값이 없습니다.  <a href='/trainer'>돌아가기</a>", 400

    sales = Sale.query.filter(Sale.trainer_name == trainer_name).all()
    if sales:
        for sale in sales:
            db.session.delete(sale)
            db.session.commit()

    # 유저가 db에 없을시 404 반환, 있을시 삭제후 리다이렉트
    trainer = Trainer.query.filter(Trainer.name == trainer_name).first()
    if not trainer:
        return "없는 트레이너입니다.  <a href='/trainer'>돌아가기</a>", 404
    else:
        db.session.delete(trainer)
        db.session.commit()

    return redirect(url_for('main.trainer_index'), code=200)