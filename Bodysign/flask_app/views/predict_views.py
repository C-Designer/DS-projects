from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request
from flask_app.models.member_model import Member
from flask_app import main_funcs as mf
from flask_app import db

bp = Blueprint('predict', __name__)


@bp.route('/pred', methods=['POST'])
def pred():
    if request.method == "POST":
        member_id = int(request.form['member_id'])
        if not member_id:
            return "값을 올바르게 기입하여 주세요.  <a href='/predict'>돌아가기</a>", 400
        
        member = Member.query.filter(Member.id == member_id).first()
        if not member:
            return "없는 회원번호입니다.  <a href='/predict'>돌아가기</a>", 400
        
        prediction, trainer_pred = mf.member_grade(member_id)
        trainers = sorted(trainer_pred.items(), key=(lambda x: x[1]), reverse = True)
    return render_template('predict.html', prediction=prediction, trainers=trainers), 200

@bp.route('/learning')
def learning():
    try:
        mf.member_grade_machine()
        mf.trainer_member_machine()
    except:
        prediction = "오류가 발생했습니다 ㅠㅠ"

    prediction = "학습을 완료하였습니다. :)"

    return render_template('predict.html', prediction=prediction), 200