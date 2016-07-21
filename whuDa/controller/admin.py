# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, request
from whuDa.controller.utils import resize_pic, requires_auth
import whuDa.model.topics as db_topics
import os
from utils import page_html


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/manage_admin/<int:page_num>')
def admin_blank():
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=.db,
                           page_size=15,
                           current_page=1,
                           url='discover/page')
    return render_template('admin/manage_admin.html')


@app.route('/admin/manage_user/<int:page_num>')
def admin_buttons():
    return render_template('admin/manage_user.html')


@requires_auth
@app.route('/admin/topic/page/<int:page_num>')
def admin_topic(page_num):
    return render_template('admin/topic.html')


@app.route('/admin/topic/add', methods=['POST'])
def admin_add_topic():
    upload_folder = 'whuDa/static/img/topic'
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    name = request.form.get('name')
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
