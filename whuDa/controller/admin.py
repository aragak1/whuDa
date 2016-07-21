# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, request
from whuDa.controller.utils import resize_pic, requires_auth, page_html
import whuDa.model.topics as db_topics
import whuDa.model.topic_question as db_topic_question
import os
import sys
from utils import page_html
import whuDa.model.users as db_users
reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


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
    upload_folder = 'whuDa/static/img/topic'
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    name = request.form.get('name')
    if not name:
        return 'empty_name'
    introduction = request.form.get('introduction')
    avatar = request.files['topic_avatar']
    if db_topics.Topics().is_exist_topic_name(name):
        return 'exist_topic'
    if avatar and '.' in avatar.filename and avatar.filename.rsplit('.', 1)[1] in allowed_extensions:
        topic_id = db_topics.Topics().add_topic(name, introduction)
        # 原图片名
        filename = name + '-max.' + avatar.filename.rsplit('.', 1)[1]
        # 裁剪后的图片名
        avatar_filename = name + '.' + avatar.filename.rsplit('.', 1)[1]
        avatar.save(os.path.join(upload_folder, filename))
        # 保存图片之后进行缩放处理
        resize_pic(os.path.join(upload_folder, filename), os.path.join(upload_folder, avatar_filename), 50, 50)
        db_topics.Topics().update_topic_url(topic_id=topic_id, topic_url='static/img/topic/' + avatar_filename)
        return 'success'
    return 'error_file'


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
    upload_folder = 'whuDa/static/img/topic'
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    name = request.form.get('name')
    if not name:
        return 'empty_name'
    introduction = request.form.get('introduction')
    avatar = request.files['topic_avatar']
    if db_topics.Topics().is_exist_topic_name(name):
        return 'exist_topic'
    if avatar and '.' in avatar.filename and avatar.filename.rsplit('.', 1)[1] in allowed_extensions:
        topic_id = db_topics.Topics().add_topic(name, introduction)
        # 原图片名
        filename = name + '-max.' + avatar.filename.rsplit('.', 1)[1]
        # 裁剪后的图片名
        avatar_filename = name + '.' + avatar.filename.rsplit('.', 1)[1]
        avatar.save(os.path.join(upload_folder, filename))
        # 保存图片之后进行缩放处理
        resize_pic(os.path.join(upload_folder, filename), os.path.join(upload_folder, avatar_filename), 50, 50)
        db_topics.Topics().update_topic_url(topic_id=topic_id, topic_url='static/img/topic/' + avatar_filename)
        return 'success'
    return 'error_file'


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
