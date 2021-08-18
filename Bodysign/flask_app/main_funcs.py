from sklearn.linear_model import LinearRegression
import joblib
import numpy as np
import pandas as pd
from flask_app.models.sale_model import Sale
from flask_app.models.machine_model import Machine
from flask_app.models.member_model import Member
from flask_app.models.trainer_model import Trainer
from flask_app import db

def member_grade_machine():
    '''
        판매값들을 모두 받아와 머신에 학습
    '''
    members = []
    target = []
    sales = Sale.query.all()

    for sale in sales:
        m = Member.query.filter(Member.id == sale.member_id).first()
        members.append([m.sex, m.age, m.real, m.roman, m.human, m.ideal, m.agent, m.relation, m.trust, m.manual, m.confidence, m.culture])
        target.append(sale.is_sale)

    feature = pd.DataFrame(data=np.array(members))
    model = LinearRegression()
    model.fit(feature, target)

    joblib.dump(model, 'model.pkl')

    # 등급 최신화
    pred = []
    member_list = Member.query.all()
    for m in member_list:
        pred.append(model.predict([[m.sex, m.age, m.real, m.roman, m.human, m.ideal, m.agent, m.relation, m.trust, m.manual, m.confidence, m.culture]]))
    
    pred = pd.Series(pred)
    q1 = pred.quantile(.25)[0]
    q2 = pred.quantile(.5)[0]
    q3 = pred.quantile(.75)[0]

    m = Machine(q1=q1, q2=q2, q3=q3)
    db.session.add(m)
    db.session.commit()


def trainer_member_machine():

    member_trainer = []
    target = []
    sales = Sale.query.all()

    for sale in sales:
        m = Member.query.filter(Member.id == sale.member_id).first()
        t = Trainer.query.filter(Trainer.name == sale.trainer_name).first()
        member_trainer.append([m.sex, m.age, m.real, m.roman, m.human, m.ideal, m.agent, m.relation, m.trust, m.manual, m.confidence, m.culture
                            ,t.sex, t.age, t.real, t.roman, t.human, t.ideal, t.agent, t.relation, t.trust, t.manual, t.confidence, t.culture])
        target.append(sale.is_sale)

    feature = pd.DataFrame(data=np.array(member_trainer))
    model = LinearRegression()
    model.fit(feature, target)

    joblib.dump(model, 'main_model.pkl')


def member_grade(member_num):
    '''
        회원번호 기입시 값을 불러와 난이도 측정
    '''
    member = Member.query.filter(Member.id == member_num).first()
    if not member:
        return "데이터 내 회원정보가 없습니다."
    
    model = joblib.load('model.pkl')

    prediction = model.predict([[member.sex, member.age, member.real, member.roman, member.human, member.ideal, member.agent, member.relation, member.trust, member.manual, member.confidence, member.culture]])[0]
    machine = Machine.query.first()

    if machine.q3 < prediction:
        prediction = "쉬움"
    elif machine.q2 < prediction:
        prediction = "보통"
    elif machine.q1 < prediction:
        prediction = "어려움"
    else:
        prediction = "매우 어려움"


    # 트레이너별 매칭 확률
    trainers = Trainer.query.all()
    main_model = joblib.load('main_model.pkl')
    trainer_pred = {}

    for t in trainers:
        predict = main_model.predict([[member.sex, member.age, member.real, member.roman, member.human, member.ideal, member.agent, member.relation, member.trust, member.manual, member.confidence, member.culture
                        ,t.sex, t.age, t.real, t.roman, t.human, t.ideal, t.agent, t.relation, t.trust, t.manual, t.confidence, t.culture]])[0]

        trainer_pred[t.name] = predict

    return prediction, trainer_pred
