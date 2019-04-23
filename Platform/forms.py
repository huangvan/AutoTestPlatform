#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
'''
@Time    : 2019/2/8 0008 20:11
@Author  : Van Huang
@Email   : huangvan0808@gmail.com
@File    : forms.py
@details : The description of the contents of the file

'''
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length


class CaseModifyForm(FlaskForm):
    title = StringField('用例', validators=[DataRequired(), Length(1, 1024)])
    server = SelectField('服务', validators=[DataRequired('请选择服务')], choices=[('QDD', 'QDD'), ('VIP', 'VIP'),
                                                                            ('MS', 'MS'), ('SOS', 'SOS'), ('OMG', 'OMG'),
                                                                            ('BK&X', 'BK&X'), ('terminal', 'terminal'),
                                                                            ('BI', 'BI'), ('ERP', 'ERP')])
    script_name = StringField('脚本名称', validators=[DataRequired(), Length(1, 256)])
    sprint = IntegerField('迭代版本', validators=[DataRequired()])
    submit = SubmitField('提交')


class CaseAddForm(FlaskForm):
    title = StringField('用例', validators=[DataRequired(), Length(1, 1024)])
    server = SelectField('服务', validators=[DataRequired('请选择服务')], choices=[('QDD', 'QDD'), ('VIP', 'VIP'),
                                                                            ('MS', 'MS'), ('SOS', 'SOS'), ('OMG', 'OMG'),
                                                                            ('BK&X', 'BK&X'), ('terminal', 'terminal'),
                                                                            ('BI', 'BI'), ('ERP', 'ERP')])
    script_name = StringField('脚本名称', validators=[DataRequired(), Length(1, 256)])
    sprint = IntegerField('迭代版本', validators=[DataRequired()])
    submit = SubmitField('提交')


class CaseMockForm(FlaskForm):
    title = StringField('用例', validators=[DataRequired(), Length(1, 1024)])
    server = SelectField('服务', validators=[DataRequired('请选择服务')], choices=[('QDD', 'QDD'), ('VIP', 'VIP'),
                                                                            ('MS', 'MS'), ('SOS', 'SOS'), ('OMG', 'OMG'),
                                                                            ('BK&X', 'BK&X'), ('terminal', 'terminal')])
    mock_status = IntegerField('是否录制', validators=[DataRequired()])
    submit = SubmitField('录制结束')


class CaseResetForm(FlaskForm):
    submit = SubmitField('重置')


class CaseScriptForm(FlaskForm):
    script = TextAreaField('脚本', validators=[DataRequired()])
    submit = SubmitField('保存')


class CaseRunForm(FlaskForm):
    submit = SubmitField('执行')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    submit = SubmitField('登录')


class UserModifyForm(FlaskForm):
    username = StringField('用户账号', validators=[DataRequired(), Length(3, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    uname = StringField('用户名称', validators=[DataRequired(), Length(1, 24)])
    userver = SelectField('所属服务', validators=[DataRequired('请选择服务')], choices=[('QDD', 'QDD'), ('VIP', 'VIP'),
                                                                            ('MS', 'MS'), ('SOS', 'SOS'), ('OMG', 'OMG'),
                                                                            ('BK&X', 'BK&X'), ('terminal', 'terminal'),
                                                                            ('BI', 'BI'), ('ERP', 'ERP')])
    submit = SubmitField('提交')


class UserADDForm(FlaskForm):
    username = StringField('用户账号', validators=[DataRequired(), Length(3, 24)])
    password = StringField('密码', validators=[DataRequired(), Length(6, 24)])
    uname = StringField('用户名称', validators=[DataRequired(), Length(1, 24)])
    userver = SelectField('所属服务', validators=[DataRequired('请选择服务')], choices=[('QDD', 'QDD'), ('VIP', 'VIP'),
                                                                            ('MS', 'MS'), ('SOS', 'SOS'), ('OMG', 'OMG'),
                                                                            ('BK&X', 'BK&X'), ('terminal', 'terminal'),
                                                                            ('BI', 'BI'), ('ERP', 'ERP')])
    submit = SubmitField('提交')
