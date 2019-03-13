#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
'''
@Time    : 2019/2/8 0008 20:07
@Author  : Van Huang
@Email   : huangvan0808@gmail.com
@File    : orm.py
@details : The description of the contents of the file

'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
