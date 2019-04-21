#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
'''
@Time    : 2019/2/8 0008 20:15
@Author  : Van Huang
@Email   : huangvan0808@gmail.com
@File    : models.py
@details : The description of the contents of the file

'''
import time

from orm import db
from flask_login import UserMixin


class CaseList(db.Model):
    __tablename__ = 'caselist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(24), nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    server = db.Column(db.String(256), nullable=False)
    mock_status = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    reset_status = db.Column(db.Integer, nullable=False)
    script_name = db.Column(db.String(256), nullable=False)
    script_name_old = db.Column(db.String(256), nullable=False)
    sprint = db.Column(db.Integer, nullable=False)
    script = db.Column(db.Text, nullable=True)
    create_time = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, user_name, title, server, mock_status, status, reset_status, script_name, script_name_old, script, sprint):
        self.user_id = user_id
        self.user_name = user_name
        self.title = title
        self.server = server
        self.mock_status = mock_status
        self.status = status
        self.reset_status = reset_status
        self.script_name = script_name
        self.script_name_old = script_name_old
        self.sprint = sprint
        self.script = script
        self.create_time = time.time()


class User(UserMixin, db.Model):
    __tablename__ = "base_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    uname = db.Column(db.String(24), nullable=False)
    userver = db.Column(db.String(256), nullable=False)
    user_status = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, uname, userver, user_status):
        self.username = username
        self.password = password
        self.uname = uname
        self.userver = userver
        self.user_status = user_status



