# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, request, session, redirect
from utils import check_mail, check_username, is_login, resize_pic, birthday_to_unix_time
import whuDa.model.users as db_users
import sys, os

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
        if username == '':
            return 'error1'
        elif email == '':
            return 'error2'
        elif password == '':
            return 'error3'
        elif repeat_password == '':
            return 'error4'
        elif password != repeat_password:
            return 'error5'
        elif not check_username(username):
            return 'error6'
        elif not check_mail(email):
            return 'error7'
        elif db_users.Users().register(username=username, password=password, email=email, last_ip=ip):
            session['username'] = username
            return 'success'
        else:
            return 'error8'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if check_mail(username):
            login_type = 'email'
        else:
            login_type = 'username'

        if username == '':
            return 'error1'
        elif password == '':
            return 'error2'
        elif db_users.Users().vaild(username, password, login_type):
            session['username'] = username
            return 'success'
        else:
            return 'false'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/user/avatar/upload', methods=['POST'])
def upload_avatar():
    if is_login():
        upload_folder = 'whuDa/static/img/avatar'
        allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
        avatar = request.files['file']
        if avatar and '.' in avatar.filename and avatar.filename.rsplit('.', 1)[1] in allowed_extensions:
            filename = session['username'] + '-max.' + avatar.filename.rsplit('.', 1)[1]
            avatar_filename = session['username'] + '.' + avatar.filename.rsplit('.', 1)[1]
            avatar.save(os.path.join(upload_folder, filename))
            # 存图片之后进行缩放处理
            resize_pic(os.path.join(upload_folder, filename), os.path.join(upload_folder, avatar_filename), 100, 100)
            db_users.Users().update_avatar_url(session['username'], 'static/img/avatar/' + avatar_filename)
        return 'success'
    return 'error'


@app.route('/user/profile/update', methods=['POST'])
def update_user_profile():
    if is_login():
        sex = int(request.form.get('sex'))
        birth_year = request.form.get('birth_year')
        birth_month = request.form.get('birth_month')
        birth_day = request.form.get('birth_day')
        birthday_unix_time = birthday_to_unix_time(birth_year, birth_month, birth_day)
        introduction = request.form.get('introduction')
        qq = str(request.form.get('qq'))
        if not qq.isdigit() or len(qq) > 11 or len(qq) < 5:
            return 'error_qq'
        mobile = str(request.form.get('mobile'))
        if not mobile.isdigit() or len(mobile) != 11:
            return 'error_mobile'
        website = request.form.get('website')
        department_id = int(request.form.get('department_id'))
    return 'error'
