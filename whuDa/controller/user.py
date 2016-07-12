# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, request
import whuDa.model.users as db_users
import sys

reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        email = request.form.get('email')
        ip = request.remote_addr
        if password != repeat_password:
            return 'error1'
        elif db_users.Users().register(username=username, password=password, email=email, last_ip=ip):
            print password
            print repeat_password
            return 'success'
        else:
            return 'error2'
