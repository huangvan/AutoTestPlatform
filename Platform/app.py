#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
'''
@Time    : 2019/2/8 0008 20:05
@Author  : Van Huang
@Email   : huangvan0808@gmail.com
@File    : app.py
@details : web application

'''
from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import CaseModifyForm, LoginForm, CaseAddForm, CaseMockForm, CaseResetForm, CaseScriptForm, CaseRunForm
from orm import db, login_manager
from models import CaseList, User
from Mock.mock import MockRecordManage
from Mock.config import base_url, host_url, wiremock_port

SECRET_KEY = 'This is my key'

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gj:xbrother@192.168.3.250/platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
mock_record = MockRecordManage(base_url, host_url, wiremock_port)


@app.route('/', methods=['GET', 'POST'])
@login_required
def show_case():
    form = CaseAddForm()
    if request.method == 'GET':
        caselists = CaseList.query.all()
        return render_template('index.html', caselists=caselists, form=form)
    else:
        if form.validate_on_submit():
            caselist = CaseList(current_user.id, current_user.username, form.title.data, form.server.data, 0, 0, 0, '')
            db.session.add(caselist)
            db.session.commit()
            flash('创建自动化测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('show_case'))


@app.route('/delete/<int:id>')
@login_required
def delete_case(id):
    caselist = CaseList.query.filter_by(id=id).first_or_404()
    db.session.delete(caselist)
    db.session.commit()
    flash('删除自动化测试用例成功!')
    return redirect(url_for('show_case'))


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_case(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseModifyForm()
        form.title.data = caselist.title
        return render_template('modify.html', form=form)
    else:
        form = CaseModifyForm()
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.title = form.title.data
            db.session.commit()
            flash('修改自动化测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('show_case'))


@app.route('/mock/<int:id>', methods=['GET', 'POST'])
@login_required
def mock_case(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseMockForm()
        return render_template('mock.html', case=caselist, form=form)
    else:
        form = CaseMockForm()
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.mock_status = 1
            db.session.commit()
            flash('用例接口脚本录制成功!')
        else:
            flash(form.errors)
        return redirect(url_for('show_case'))


@app.route('/record/<int:id>', methods=['GET', 'POST'])
@login_required
def record_case(id):
    if request.method == 'GET':
        flash('请开始在环境进行该用例操作，操作结束后点击“结束录制”按钮生成脚本！')
        mock_record.start_record()
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseMockForm()
        return render_template('mock.html', case=caselist, form=form)
    else:
        mock_record.stop_record()
        flash('停止录制成功!')
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseAddForm()
        return render_template('run.html', case=caselist, form=form)


@app.route('/stop/<int:id>', methods=['GET', 'POST'])
@login_required
def stop_record(id):
    if request.method == 'GET':
        mock_record.stop_record()
        flash('停止录制成功，已经生成自动化脚本!')
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseAddForm()
        return render_template('run.html', case=caselist, form=form)
    else:
        flash('HTTP方法错误!')
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseMockForm()
        return render_template('mock.html', case=caselist, form=form)


@app.route('/run/<int:id>', methods=['GET', 'POST'])
@login_required
def run_case(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseAddForm()
        return render_template('run.html', case=caselist, form=form)
    else:
        form = CaseRunForm()
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.status = 1
            db.session.commit()
            flash('脚本执行成功!')
        else:
            flash(form.errors)
        return redirect(url_for('show_case'))


@app.route('/script/<int:id>', methods=['GET', 'POST'])
@login_required
def case_script(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseAddForm()
        return render_template('run.html', case=caselist, form=form)
    else:
        form = CaseScriptForm()
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.script = form.script.data
            caselist.mock_status = 1
            db.session.commit()
            flash('脚本保存成功!')
        else:
            flash(form.errors)
        return redirect(url_for('run_case', id=id))


@app.route('/reset/<int:id>', methods=['GET', 'POST'])
@login_required
def reset_case(id):
    form = CaseResetForm()
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        return render_template('reset.html', case=caselist, form=form)
    else:
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.mock_status = 0
            caselist.status = 0
            caselist.reset_status = 1
            caselist.script = ''
            db.session.commit()
            flash('重置测试用例回初始状态成功!')
        else:
            flash(form.errors)
        return redirect(url_for('show_case'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('欢迎登录自动化测试系统!')
            return redirect(url_for('show_case'))
        else:
            flash('无效的用户名或者密码!')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
