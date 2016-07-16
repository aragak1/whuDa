# -*- coding: utf-8 -*-
from whuDa import db
'''department_id int(10) not null auto_increment comment '学院ID',
    name varchar(32) not null comment '学院名','''


class Department(db.Model):
    __tablename__ = 'department'

    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def get_all_department(self):
        return Department.query.all()