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
import os
import math
import json
import logging
from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import CaseModifyForm, LoginForm, CaseAddForm, CaseMockForm, CaseResetForm, CaseScriptForm, CaseRunForm, \
    UserModifyForm, UserADDForm
from orm import db, login_manager
from models import CaseList, User
from Mock.mock import MockRecordManage
from Mock.config import base_url, wiremock_url, wiremock_port

SECRET_KEY = 'This is my key'

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gj:xbrother@192.168.3.250/platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

mock_record = MockRecordManage(base_url, wiremock_url, wiremock_port)


# 公共部分
def get_page(total, p):
    show_page = 5   # 显示的页码数
    page_offset = 2  # 偏移量
    start = 1    # 分页条开始
    end = total  # 分页条结束

    if total > show_page:
        if p > page_offset:
            start = p - page_offset
            if total > p + page_offset:
                end = p + page_offset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
        if p + page_offset > total:
            start = start - (p + page_offset - end)
    # 用于模版中循环
    dic = range(start, end + 1)
    return dic


# 统计服务维度的用例情况
def get_server_data(server):
    list_count = []
    case_count = CaseList.query.filter_by(server=server).count()
    list_count.append(case_count)
    mock_count = CaseList.query.filter(CaseList.server == server, CaseList.mock_status == 1).count()
    list_count.append(mock_count)
    run_count = CaseList.query.filter(CaseList.server == server, CaseList.status > 0).count()
    list_count.append(run_count)
    pass_count = CaseList.query.filter(CaseList.server == server, CaseList.status == 1).count()
    list_count.append(pass_count)
    if case_count == 0:
        list_count.append('0.00%')
        list_count.append('0.00%')
    else:
        list_count.append("%.2f%%" % (run_count / case_count * 100))
        list_count.append("%.2f%%" % (pass_count / case_count * 100))
    return list_count


# 统计用户维度的用例情况
def get_user_data(username):
    list_count = []
    case_count = CaseList.query.filter_by(user_name=username).count()
    list_count.append(case_count)
    mock_count = CaseList.query.filter(CaseList.user_name == username, CaseList.mock_status == 1).count()
    list_count.append(mock_count)
    run_count = CaseList.query.filter(CaseList.user_name == username, CaseList.status > 0).count()
    list_count.append(run_count)
    pass_count = CaseList.query.filter(CaseList.user_name == username, CaseList.status == 1).count()
    list_count.append(pass_count)
    if case_count == 0:
        list_count.append('0.00%')
        list_count.append('0.00%')
    else:
        list_count.append("%.2f%%" % (run_count / case_count * 100))
        list_count.append("%.2f%%" % (pass_count / case_count * 100))
    return list_count


# 统计迭代维度的用例情况
def get_sprint_data(server):
    list_count = []
    case_count = CaseList.query.filter_by(server=server).count()
    list_count.append(case_count)
    mock_count = CaseList.query.filter(CaseList.server == server, CaseList.mock_status == 1).count()
    list_count.append(mock_count)
    run_count = CaseList.query.filter(CaseList.server == server, CaseList.status > 0).count()
    list_count.append(run_count)
    pass_count = CaseList.query.filter(CaseList.server == server, CaseList.status == 1).count()
    list_count.append(pass_count)
    if case_count == 0:
        list_count.append('0.00%')
        list_count.append('0.00%')
    else:
        list_count.append("%.2f%%" % (run_count / case_count * 100))
        list_count.append("%.2f%%" % (pass_count / case_count * 100))
    return list_count


# 工作台
@app.route('/')
@login_required
def show_work():
    if request.method == 'GET':
        return render_template('work.html')


@app.route('/query/server/', methods=['POST'])
@login_required
def show_server_data():
    server_list = ['QDD', 'SOS', 'terminal', 'BK&X', 'VIP', 'MS', 'OMG', 'BI']
    info = request.values
    limit = info.get('limit', 5)
    offset = info.get('offset', 0)
    order = info.get('order', 'asc')
    total = len(server_list)
    data = []
    for server in server_list:
        dic = {}
        lis = get_server_data(server)
        dic['server_name'] = server
        dic['case_count'] = lis[0]
        dic['mock_count'] = lis[1]
        dic['run_count'] = lis[2]
        dic['pass_count'] = lis[3]
        dic['run_rate'] = lis[4]
        dic['pass_rate'] = lis[5]
        data.append(dic)
    return json.dumps({'total': total, 'rows': data[int(offset):(int(offset) + int(limit))]})


@app.route('/query/user/', methods=['POST'])
@login_required
def show_user_data():
    all_user = User.query.all()
    info = request.values
    limit = info.get('limit', 5)
    offset = info.get('offset', 0)
    order = info.get('order', 'asc')
    total = User.query.count()
    data = []
    for user in all_user:
        logging.debug(user.username)
        dic = {}
        user_list = get_user_data(user.username)
        dic['name'] = user.username
        dic['case_count'] = user_list[0]
        dic['mock_count'] = user_list[1]
        dic['run_count'] = user_list[2]
        dic['pass_count'] = user_list[3]
        dic['run_rate'] = user_list[4]
        dic['pass_rate'] = user_list[5]
        data.append(dic)
    return json.dumps({'total': total, 'rows': data[int(offset):(int(offset) + int(limit))]})


@app.route('/test/')
@login_required
def test_html():
    return render_template("test.html")


# 功能测试
@app.route('/function/', methods=['GET', 'POST'])
@login_required
def show_fuction():
    form = CaseAddForm()
    if request.method == 'GET':
        return redirect(url_for('case_list', p=1))
    else:
        if form.validate_on_submit():
            casename = CaseList.query.filter_by(script_name=form.script_name.data).count()
            if casename != 0:
                flash('脚本名称重复，请重新添加!')
            else:
                caselist = CaseList(current_user.id, current_user.username, form.title.data, form.server.data, 0, 0, 0, form.script_name.data, form.script_name.data, form.sprint.data, '')
                db.session.add(caselist)
                db.session.commit()
                flash('创建自动化测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('case_list', p=1))


@app.route('/function/case/<int:p>', methods=['GET', 'POST'])
@login_required
def case_list(p):
    form = CaseAddForm()
    if request.method == 'GET':
        show_index_status = 0   # 显示首页状态
        if p == '':
            p = 1
        else:
            p = int(p)
            if p > 1:
                show_index_status = 1

        limit_start = (int(p)-1)*10  # 起始
        caselists = CaseList.query.limit(10).offset(limit_start).all()
        count = CaseList.query.count()   # 总记录
        total = int(math.ceil(count/10.0))  # 总页数

        dic = get_page(total, p)
        page_data = {
            'user_list': caselists,
            'p': int(p),
            'total': total,
            'show_index_status': show_index_status,
            'dic_list': dic
        }
        return render_template("index.html", caselists=caselists, form=form, page_data=page_data)
    else:
        if form.validate_on_submit():
            casename = CaseList.query.filter_by(script_name=form.script_name.data).count()
            if casename != 0:
                flash('脚本名称重复，请重新添加!')
            else:
                caselist = CaseList(current_user.id, current_user.username, form.title.data, form.server.data, 0, 0, 0, form.script_name.data, form.script_name.data, form.sprint.data, '')
                db.session.add(caselist)
                db.session.commit()
                flash('创建自动化测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('case_list', p=p))


@app.route('/delete/<int:id>')
@login_required
def delete_case(id):
    caselist = CaseList.query.filter_by(id=id).first_or_404()
    mock_record.delete_file(caselist.script_name, caselist.server)
    db.session.delete(caselist)
    db.session.commit()
    flash('删除自动化测试用例成功!')
    return redirect(url_for('case_list', p=1))


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_case(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseModifyForm()
        form.title.data = caselist.title
        form.script_name.data = caselist.script_name
        form.sprint.data = caselist.sprint
        return render_template('modify.html', form=form)
    else:
        form = CaseModifyForm()
        if form.validate_on_submit():
            casename = CaseList.query.filter_by(script_name=form.script_name.data).count()
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            if casename != 0 and form.script_name.data != caselist.script_name:
                flash('脚本名称重复，请重新修改!')
                return redirect(url_for('change_case', id=id))
            else:
                caselist.title = form.title.data
                caselist.script_name_old = caselist.script_name
                caselist.script_name = form.script_name.data
                caselist.sprint = form.sprint.data
                db.session.commit()
                if caselist.script_name != caselist.script_name_old:
                    mock_record.change_file(caselist.script_name, caselist.script_name_old, caselist.server)
                flash('修改自动化测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('change_case', id=id))


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
        return redirect(url_for('mock_case', id=id))


@app.route('/record/<int:id>', methods=['GET', 'POST'])
@login_required
def record_case(id):
    if request.method == 'GET':
        flash('请开始在环境进行该用例操作，操作结束后点击“结束录制”按钮生成脚本！')
        mock_record.start_record()
        return redirect(url_for('mock_case', id=id))
    else:
        flash('HTTP方法错误!')
        return redirect(url_for('mock_case', id=id))


@app.route('/stop/<int:id>', methods=['GET', 'POST'])
@login_required
def stop_record(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseScriptForm()
        mock_record.create_file(caselist.script_name, caselist.server)
        mock_record.stop_record()
        if os.path.exists(mock_record.mock_case_name):
            with open(mock_record.mock_case_name, 'r', encoding='utf-8') as f:
                sql = ''.join(f.readlines())
                caselist.script = sql
        db.session.commit()
        flash('停止录制成功，已经生成自动化脚本!')
        return redirect(url_for('run_case', id=id))
        # return render_template('run.html', case=caselist, form=form)
    else:
        flash('HTTP方法错误!')
        return redirect(url_for('mock_case', id=id))


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
            flash('脚本已经执行，请查看结果!')
        else:
            flash(form.errors)
        return redirect(url_for('run_case', id=id))


@app.route('/git/<int:id>', methods=['GET', 'POST'])
@login_required
def git_case(id):
    if request.method == 'GET':
        caselist = CaseList.query.filter_by(id=id).first_or_404()
        form = CaseAddForm()
        return render_template('git.html', case=caselist, form=form)
    else:
        form = CaseScriptForm()
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.script = form.script.data
            caselist.mock_status = 1
            db.session.commit()
            mock_record.create_file(caselist.script_name, caselist.server)
            mock_record.update_case(form.script.data)
            flash('脚本更新成功!')
        else:
            flash(form.errors)
        return redirect(url_for('git_case', id=id))


@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update_case(id):
    if request.method == 'POST':
        form = CaseScriptForm()
        if form.validate_on_submit():
            caselist = CaseList.query.filter_by(id=id).first_or_404()
            caselist.script = form.script.data
            caselist.mock_status = 1
            db.session.commit()
            mock_record.create_file(caselist.script_name, caselist.server)
            mock_record.update_case(form.script.data)
            flash('脚本更新成功!')
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
        return redirect(url_for('reset_case', id=id))


# 契约测试
@app.route('/contract/', methods=['GET', 'POST'])
@login_required
def show_contract():
    form = CaseAddForm()
    if request.method == 'GET':
        return redirect(url_for('case_contract', p=1))
    else:
        if form.validate_on_submit():
            casename = CaseList.query.filter_by(script_name=form.script_name.data).count()
            print(form.script_name.data, casename)
            if casename != 0:
                flash('脚本名称重复，请重新添加!')
            else:
                caselist = CaseList(current_user.id, current_user.username, form.title.data, form.server.data, 0, 0, 0, form.script_name.data, form.script_name.data, '')
                db.session.add(caselist)
                db.session.commit()
                flash('创建契约测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('case_contract', p=1))


@app.route('/contract/case/<int:p>', methods=['GET', 'POST'])
@login_required
def case_contract(p):
    form = CaseAddForm()
    if request.method == 'GET':
        show_index_status = 0   # 显示首页状态
        if p == '':
            p = 1
        else:
            p = int(p)
            if p > 1:
                show_index_status = 1

        limit_start = (int(p)-1)*10  # 起始
        caselists = CaseList.query.limit(10).offset(limit_start).all()
        count = CaseList.query.count()   # 总记录
        total = int(math.ceil(count/10.0))  # 总页数

        dic = get_page(total, p)
        page_data = {
            'user_list': caselists,
            'p': int(p),
            'total': total,
            'show_index_status': show_index_status,
            'dic_list': dic
        }
        return render_template("contract.html", caselists=caselists, form=form, page_data=page_data)
    else:
        if form.validate_on_submit():
            casename = CaseList.query.filter_by(script_name=form.script_name.data).count()
            if casename != 0:
                flash('脚本名称重复，请重新添加!')
            else:
                caselist = CaseList(current_user.id, current_user.username, form.title.data, form.server.data, 0, 0, 0, form.script_name.data, form.script_name.data, '')
                db.session.add(caselist)
                db.session.commit()
                flash('创建契约测试用例成功!')
        else:
            flash(form.errors)
        return redirect(url_for('case_contract', p=p))


# 平台管理
@app.route('/manage/', methods=['GET'])
@login_required
def show_manage():
    form = UserModifyForm()
    all_user = User.query.all()
    return render_template('manage.html', all_user=all_user, form=form)


@app.route('/add/user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserADDForm()
    if request.method == 'GET':
        return render_template('modify_user.html', form=form)
    else:
        if form.validate_on_submit():
            user_exit = User.query.filter_by(username=form.username.data).first()
            if not user_exit:
                userlist = User(form.username.data, form.password.data, form.uname.data, form.userver.data, 1)
                db.session.add(userlist)
                db.session.commit()
                flash('用户添加成功!')
            else:
                flash('用户已经存在!')
                return redirect(url_for('add_user'))
        else:
            flash(form.errors)
        return redirect(url_for('show_manage'))


@app.route('/change/<username>', methods=['GET', 'POST'])
@login_required
def change_user(username):
    form = UserModifyForm()
    if request.method == 'GET':
        userlist = User.query.filter_by(username=username).first_or_404()
        form.username.data = userlist.username
        form.uname.data = userlist.uname
        form.userver.data = userlist.userver
        form.password.data = userlist.password
        return render_template('modify_user.html', form=form)
    else:
        if form.validate_on_submit():
            userlist = User.query.filter_by(username=username).first_or_404()
            # userlist.username = form.username.data
            userlist.uname = form.uname.data
            userlist.userver = form.userver.data
            userlist.password = form.password.data
            db.session.commit()
            flash('修改用户信息成功!')
        else:
            flash(form.errors)
        return redirect(url_for('change_user', username=username))


@app.route('/disable/<username>')
@login_required
def disable_user(username):
    userlist = User.query.filter_by(username=username).first_or_404()
    if userlist.user_status:
        status = 0
    else:
        status = 1
    userlist.user_status = status
    db.session.commit()
    flash('修改用户状态成功!')
    return redirect(url_for('show_manage'))


# 用户管理
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password'], user_status=1).first()
        if user:
            login_user(user)
            flash('欢迎登录自动化测试系统!')
            return redirect(url_for('show_work'))
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
