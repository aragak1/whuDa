# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/manage_admin')
def admin_blank():
    return render_template('admin/manage_admin.html.html')


@app.route('/admin/manage_user')
def admin_buttons():
    return render_template('admin/manage_user.html')


@app.route('/admin/topic')
def admin_topic():
    return render_template('admin/topic.html')
