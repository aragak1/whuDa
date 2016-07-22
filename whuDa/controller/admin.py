# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, request
from whuDa.controller.utils import resize_pic, requires_auth, page_html
import whuDa.model.topics as db_topics
import whuDa.model.topic_question as db_topic_question
import os
import sys
from utils import page_html, check_mail, check_username, birthday_to_unix_time
import whuDa.model.users as db_users
reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


@app.template_filter('timeformat')
def timeformat_filter(t, format):
    import time
    return time.strftime(format, time.localtime(int(t)))


@app.route('/admin/manage_admin/page/<int:page_num>')
def manage_admin(page_num):
    pagination = page_html(total_count=db_users.Users().get_admin_count(),
                           page_size=15,
                           current_page=page_num,
                           url='admin/manage_admin/page')
    return render_template('/admin/manage_admin.html',
                           admin_datas=db_users.Users().get_admins_by_page(page_num, 15),
                           pagination=pagination)


@app.route('/admin/manage_admin/add', methods=['POST'])
def admin_add_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    sex = request.form.get('sex')
    birthday_y = request.form.get('birthday_y')
    birthday_m = request.form.get('birthday_m')
    birthday_d = request.form.get('birthday_d')
    department_id = request.form.get('department_id')
    brief = request.form.get('brief')
    email = request.form.get('email')
    qq = request.form.get('qq')
    phone = request.form.get('phone')
    website = request.form.get('website')
    if db_users.Users().is_exist_username(username):
        return render_template('jump.html', title="添加失败", text='该用户名已存在', url='/admin/manage_admin/page/1')
    if db_users.Users().is_exist_email(email):
        return render_template('jump.html', title="添加失败", text='邮箱已被使用', url='/admin/manage_admin/page/1')
    db_users.Users().add_user(username=username, password=password, sex=sex,
                              birthday=birthday_to_unix_time(birthday_y, birthday_m, birthday_d),
                              department_id=department_id, introduction=brief,
                              email=email, qq=qq, phone=phone, website=website, group_id=0)
    return render_template('jump.html', title="添加成功", text='普通用户添加成功', url='/admin/manage_admin/page/1')


@app.route('/admin/manage_user/page/<int:page_num>')
def manage_user(page_num):
    pagination = page_html(total_count=db_users.Users().get_general_user_count(),
                           page_size=15,
                           current_page=page_num,
                           url='admin/manage_user/page')
    return render_template('/admin/manage_user.html',
                           user_datas=db_users.Users().get_general_user_by_page(page_num, 15),
                           pagination=pagination)


@app.route('/admin/manage_user/add', methods=['POST'])
def admin_add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    sex = request.form.get('sex')
    birthday_y = request.form.get('birthday_y')
    birthday_m = request.form.get('birthday_m')
    birthday_d = request.form.get('birthday_d')
    department_id = request.form.get('department_id')
    brief = request.form.get('brief')
    email = request.form.get('email')
    qq = request.form.get('qq')
    phone = request.form.get('phone')
    website = request.form.get('website')
    if db_users.Users().is_exist_username(username):
        return render_template('jump.html', title="添加失败", text='该用户名已存在', url='/admin/manage_user/page/1')
    if db_users.Users().is_exist_email(email):
        return render_template('jump.html', title="添加失败", text='邮箱已被使用', url='/admin/manage_user/page/1')
    db_users.Users().add_user(username=username, password=password, sex=sex,
                              birthday=birthday_to_unix_time(birthday_y, birthday_m, birthday_d),
                              department_id=department_id, introduction=brief,
                              email=email, qq=qq, phone=phone, website=website, group_id=2)
    return render_template('jump.html', title="添加成功", text='普通用户添加成功', url='/admin/manage_user/page/1')


@app.route('/admin/topic/page/<int:page_num>')
def admin_topic(page_num):
    total_count = db_topics.Topics().get_topic_count()
    pagination = page_html(total_count=total_count, page_size=15, current_page=page_num, url='admin/topic/page')
    topics = db_topics.Topics().get_raw_topics_by_page(page_num=page_num, page_size=15)
    return render_template('admin/topic.html', topics=topics, pagination=pagination)


# form直接提交
@app.route('/admin/topic/add', methods=['POST'])
def admin_add_topic():
    upload_folder = 'whuDa/static/img/topic'
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    name = request.form.get('name')
    if not name:
        return render_template('jump.html', title="添加失败", text='话题名不能为空', url='/admin/topic/page/1')
    introduction = request.form.get('introduction')
    avatar = request.files['topic_avatar']
    if db_topics.Topics().is_exist_topic_name(name):
        return render_template('jump.html', title="添加失败", text='话题已经存在', url='/admin/topic/page/1')
    if avatar:
        if '.' in avatar.filename and avatar.filename.rsplit('.', 1)[1] in allowed_extensions:
            # 原图片名
            filename = name + '-max.' + avatar.filename.rsplit('.', 1)[1]
            # 裁剪后的图片名
            avatar_filename = name + '.' + avatar.filename.rsplit('.', 1)[1]
            avatar.save(os.path.join(upload_folder, filename))
            # 保存图片之后进行缩放处理
            resize_pic(os.path.join(upload_folder, filename), os.path.join(upload_folder, avatar_filename), 50, 50)
            # 添加话题
            topic_id = db_topics.Topics().add_topic(name, introduction)
            db_topics.Topics().update_topic_url(topic_id=topic_id, topic_url='static/img/topic/' + avatar_filename)
            return render_template('jump.html', title="添加成功", text='话题添加成功', url='/admin/topic/page/1')
        else:
            return render_template('jump.html', title="添加失败", text='不支持的文件格式', url='/admin/topic/page/1')
    db_topics.Topics().add_topic(name, introduction)
    return render_template('jump.html', title="添加成功", text='话题添加成功', url='/admin/topic/page/1')


# form直接提交
@app.route('/admin/topic/update', methods=['POST'])
def admin_update_topic():
    upload_folder = 'whuDa/static/img/topic'
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    name = request.form.get('name')
    topic_id = request.form.get('topic_id')
    if not name:
        return render_template('jump.html',
                               title='修改失败',
                               text='话题名不能为空',
                               url='/admin/topic/' + topic_id)
    introduction = request.form.get('introduction')
    avatar = request.files['topic_avatar']

    # 修改话题名字和介绍
    db_topics.Topics().update_topic(topic_id, name, introduction)

    # 上传了图片
    if avatar:
        if '.' in avatar.filename and avatar.filename.rsplit('.', 1)[1] in allowed_extensions:
            # 原图片名
            filename = name + '-max.' + avatar.filename.rsplit('.', 1)[1]
            # 裁剪后的图片名
            avatar_filename = name + '.' + avatar.filename.rsplit('.', 1)[1]
            avatar.save(os.path.join(upload_folder, filename))
            # 保存图片之后进行缩放处理
            resize_pic(os.path.join(upload_folder, filename), os.path.join(upload_folder, avatar_filename), 50, 50)
            db_topics.Topics().update_topic_url(topic_id=topic_id, topic_url='static/img/topic/' + avatar_filename)
        else:
            return render_template('jump.html',
                                   title='修改失败',
                                   text='不支持的文件格式',
                                   url='/admin/topic/' + topic_id)
    return render_template('jump.html',
                           title='修改成功',
                           text='话题修改成功',
                           url='/admin/topic/page/1')


# js提交
@app.route('/admin/topic/delete', methods=['POST'])
def admin_delete_topic():
    topic_id = request.form.get('topic_id')
    if db_topic_question.Topic_question().get_question_count(topic_id=topic_id):
        return 'not_null'
    if db_topics.Topics().is_exist_topic_id(topic_id):
        db_topics.Topics().delete_topic(topic_id)
        return 'success'
    return 'error'


@app.route('/admin/topic/<int:topic_id>')
def admin_topic_detail(topic_id):
    topic = db_topics.Topics().get_topic_by_id(topic_id)
    return render_template('admin/update_topic.html', topic=topic)


@app.route('/admin/manage_admin/<int:uid>')
def admin_detail(uid):
    from utils import get_date
    import time
    import whuDa.model.department as db_department
    user = db_users.Users().get_user_by_id(uid)
    dates = {
        'year': [y for y in range(1900, 1 + get_date(time.time())['year'])],
        'month': [m for m in range(1, 13)],
        'day': [d for d in range(1, 32)]}
    birthday = db_users.Users().get_birthday_dict(uid)
    departments = db_department.Department().get_all_department()
    return render_template('admin/update_admin.html',
                           user=user,
                           dates=dates,
                           birthday=birthday,
                           departments=departments)


@app.route('/admin/manage_user/<int:uid>')
def general_user_detail(uid):
    from utils import get_date
    import time
    import whuDa.model.department as db_department
    user = db_users.Users().get_user_by_id(uid)
    dates = {
        'year': [y for y in range(1900, 1 + get_date(time.time())['year'])],
        'month': [m for m in range(1, 13)],
        'day': [d for d in range(1, 32)]}
    birthday = db_users.Users().get_birthday_dict(uid)
    departments = db_department.Department().get_all_department()
    return render_template('admin/update_general_user.html',
                           user=user,
                           dates=dates,
                           birthday=birthday,
                           departments=departments)


@app.route('/admin/manage_admin/update', methods=['POST'])
def admin_update_admin():
    uid = request.form.get('uid')
    username = request.form.get('username')
    sex = request.form.get('sex')
    birthday_y = request.form.get('birthday_y')
    birthday_m = request.form.get('birthday_m')
    birthday_d = request.form.get('birthday_d')
    department_id = request.form.get('department_id')
    brief = request.form.get('brief')
    email = request.form.get('email')
    qq = request.form.get('qq')
    phone = request.form.get('phone')
    website = request.form.get('website')
    if db_users.Users().is_username_used_by_other(uid, username):
        return render_template('jump.html', title="更改失败", text='该用户名已存在', url='/admin/manage_admin/page/1')
    if db_users.Users().is_email_used_by_other(uid, email):
        return render_template('jump.html', title="更改失败", text='邮箱已被使用', url='/admin/manage_admin/page/1')
    db_users.Users().update_user(uid=uid, username=username, sex=sex,
                                 birthday=birthday_to_unix_time(birthday_y, birthday_m, birthday_d),
                                 department_id=department_id, introduction=brief,
                                 email=email, qq=qq, phone=phone, website=website)
    return render_template('jump.html', title="更改成功", text='管理员信息修改成功', url='/admin/manage_admin/page/1')


@app.route('/admin/manage_user/update', methods=['POST'])
def admin_update_user():
    uid = request.form.get('uid')
    username = request.form.get('username')
    sex = request.form.get('sex')
    birthday_y = request.form.get('birthday_y')
    birthday_m = request.form.get('birthday_m')
    birthday_d = request.form.get('birthday_d')
    department_id = request.form.get('department_id')
    brief = request.form.get('brief')
    email = request.form.get('email')
    qq = request.form.get('qq')
    phone = request.form.get('phone')
    website = request.form.get('website')
    if db_users.Users().is_username_used_by_other(uid, username):
        return render_template('jump.html', title="更改失败", text='该用户名已存在', url='/admin/manage_user/page/1')
    if db_users.Users().is_email_used_by_other(uid, email):
        return render_template('jump.html', title="更改失败", text='邮箱已被使用', url='/admin/manage_user/page/1')
    db_users.Users().update_user(uid=uid, username=username, sex=sex,
                                 birthday=birthday_to_unix_time(birthday_y, birthday_m, birthday_d),
                                 department_id=department_id, introduction=brief,
                                 email=email, qq=qq, phone=phone, website=website)
    return render_template('jump.html', title="更改成功", text='普通用户信息修改成功', url='/admin/manage_user/page/1')


@app.route('/admin/user/delete', methods=['POST'])
def admin_delete_user():
    uid = request.form.get('uid')
    db_users.Users().delete_user(uid)
    return 'success'


@app.route('/admin/update_password_page/<int:flag>/<int:uid>')
def admin_update_password(flag, uid):
    return render_template('admin/update_password.html', flag=flag, uid=uid)


@app.route('/admin/update_password', methods=['POST'])
def update_pwd():
    uid = request.form.get('uid')
    old_pwd = request.form.get('old_pwd')
    new_pwd = request.form.get('new_pwd')
    print db_users.Users().check_pwd(uid, old_pwd)
    if not db_users.Users().check_pwd(uid, old_pwd):
        return 'error'
    else:
        db_users.Users().update_pwd(uid, new_pwd)
        return 'success'
