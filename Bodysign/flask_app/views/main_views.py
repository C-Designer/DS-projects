from flask import Blueprint, render_template, redirect, request
from flask_paginate import Pagination, get_page_parameter
from flask_app.models.machine_model import Machine
from flask_app.models.sale_model import Sale
from flask_app.models.member_model import Member
from flask_app.models.trainer_model import Trainer
from flask_app import db
import numpy as np

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html'), 200


@bp.route('/predict')
def predict_index():
    return render_template('predict.html'), 200


@bp.route('/member/')
def member_index():
    page = request.args.get('page', 1, type=int)
    members = Member.query.paginate(page=page, per_page=10)

    return render_template('member.html', members=members)


@bp.route('/trainer')
def trainer_index():
    page = request.args.get('page', 1, type=int)
    trainers = Trainer.query.paginate(page=page, per_page=10)

    return render_template('trainer.html', trainers=trainers)


@bp.route('/sale')
def sale_index():
    page = request.args.get('page', 1, type=int)
    sales = Sale.query.paginate(page=page, per_page=10)
    trainers = Trainer.query.all()

    return render_template('sale.html', sales=sales, trainers=trainers)

@bp.route('/sale/search/', methods=['POST'])
def search():

    trainer_name = str(request.form['trainer_name'])
    if not trainer_name:
        return "None", 400

    page = request.args.get('page', 1, type=int)
    sales = Sale.query.filter(Sale.trainer_name == trainer_name).paginate(page=page, per_page=10)
    trainers = Trainer.query.all()

    return render_template('sale.html', sales=sales, trainers=trainers)
    

@bp.route('/data')
def insert_data():
    # member
    li = []
    for i in range(0, 1000):
        l = []
        for j in range(0, 12):
            if j > 0:
                rd = np.random.randint(0, 100) # wpi 0 ~ 99
            elif i == 1:
                rd = np.random.randint(10, 80) # age 10 ~ 80
            else:
                rd = np.random.randint(1, 3) # sex [1, 2]
            l.append(rd)
        li.append(l)
    
    for i in li:
        member = Member(sex=i[0], age=i[1], real=i[2], roman=i[3], human=i[4], ideal=i[5], agent=i[6], relation=i[7], trust=i[8], manual=i[9], confidence=i[10], culture=i[11])
        db.session.add(member)

    # trainer
    name = ['cd', 'bj', 'tom', 'kevin', 'chris', 'hani', 'jason', 'jerry', 'jerome', 'baro', 'peter', 'kelly', 'jun']

    li = []
    for n in name:
        l = []
        l.append(n)
        for i in range(0, 12):
            if i > 1:
                rd = np.random.randint(0, 100)
            elif i == 1:
                rd = np.random.randint(20, 40)
            else:
                rd = np.random.randint(1, 3)
            l.append(rd)
        li.append(l)

    for i in li:
        trainer = Trainer(name=i[0], sex=i[1], age=i[2], real=i[3], roman=i[4], human=i[5], ideal=i[6], agent=i[7], relation=i[8], trust=i[9], manual=i[10], confidence=i[11], culture=i[12])
        db.session.add(trainer)

    # sale
    for i in range(0, 100000):
        if i < 30000:
            is_sale = 1
        else:
            is_sale = 0
        trainer_name = name[np.random.randint(0, len(name))]
        member_id = np.random.randint(1, 1000)
        
        sale = Sale(is_sale=is_sale, trainer_name=trainer_name, member_id=member_id)
        db.session.add(sale)
    
    db.session.commit()    
    return render_template('index.html'), 200