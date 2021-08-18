from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask_app.models.sale_model import Sale
from flask_app.models.member_model import Member
from flask_app import db

bp = Blueprint('sale', __name__)

@bp.route('/sale/', methods=['POST'])
def add_sale():

    if request.method == "POST":
        try:
            member_id = int(request.form['member_id'])
            is_sale = int(request.form['is_sale'])
            trainer_name = str(request.form['trainer_name'])
        except:
            return "모든 값을 올바르게 기입하여 주세요.  <a href='/sale'>돌아가기</a>", 400

        # member_id가 있는지 확인
        member = Member.query.filter(Member.id == member_id).first()
        if not member:
            return "없는 회원번호 입니다. <a href='/sale'>돌아가기</a>", 400
        
        sale = Sale(is_sale=is_sale, member_id=member_id, trainer_name=trainer_name)
        db.session.add(sale)
        db.session.commit()

        return redirect(url_for('main.sale_index'), code=200)

@bp.route('/sale/', defaults={ 'sale_id' : None })
@bp.route('/sale/<int:sale_id>')
def delete_sale(sale_id):
    # 던진 값이 없을시 404 반환
    if not sale_id:
        return 'None', 400

    sales = Sale.query.filter(Sale.id == sale_id).all()
    if sales:
        for sale in sales:
            db.session.delete(sale)
            db.session.commit()

    return redirect(url_for('main.sale_index'), code=200)