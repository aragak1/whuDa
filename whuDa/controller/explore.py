# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, redirect, session
from utils import is_login, get_discover_datas, page_html, get_hot_datas, get_wait_reply_datas
import whuDa.model.users as db_users
import whuDa.model.questions as db_questions
import whuDa.model.topics as db_topics
import whuDa.model.topic_focus as db_topic_focus
import sys

reload(sys)
sys.setdefaultencoding('utf8')


'''
    渲染需要的数据:
    判断page，根据page返回问题的list
    问题标题，问题id （questions）
    问题的最新回复者/发起者 (user)
    问题关注人数 (question_focus)
    问题回复数 (answers)
    问题浏览次数 (questions)
    问题发布时间 (questions)
'''


# 登陆前后的index页面都是发现页面
@app.route('/')
def index():
    if is_login():
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        focus_topics = db_topic_focus.Topic_focus().get_user_focus_topics(user.uid)
        pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                               page_size=15,
                               current_page=1,
                               url='discover/page')
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=1, page_size=15),
                               pagenation=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users,
                               focus_topics=focus_topics)
    return render_template('index.html')


@app.route('/discover/page/<int:page_num>')
def discover(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=page_num,
                           url='discover/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        focus_topics = db_topic_focus.Topic_focus().get_user_focus_topics(user.uid)
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=page_num, page_size=15),
                               pagenation=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users,
                               focus_topics=focus_topics)
    return render_template('index.html')


@app.route('/hot/page/<int:page_num>')
def hot_page(page_num):
    if is_login():
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        pagenation = page_html(total_count=db_questions.Questions().get_questions_count(),
                               page_size=15,
                               current_page=page_num,
                               url='hot/page')
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=page_num, page_size=15),
                               pagenation=pagenation,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('hot_questions.html')


@app.route('/wait-reply/page/<int:page_num>')
def wait_reply_page(page_num):
    if is_login():
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        pagenation = page_html(total_count=db_questions.Questions().get_wait_reply_questions_count(),
                               page_size=15,
                               current_page=page_num,
                               url='wait-reply/page')
        return render_template('login/login-wait_reply.html',
                               user=user,
                               datas=get_wait_reply_datas(page_num=page_num, page_size=15),
                               pagenation=pagenation,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('wait_reply.html')


@app.route('/dynamic')
def dynamic():
    if is_login():
        return render_template('login/login-dynamic.html')
    return redirect('/')


@app.route('/notifications')
def notifications():
    if is_login():
        return render_template('login/notifications.html')
    return redirect('/')


@app.route('/message')
def message():
    if is_login():
        return render_template('login/message.html')
    return redirect('/')


@app.route('/help')
def help():
    if is_login():
        return render_template('login/login-help.html')
    return render_template('help.html')


@app.route('/about')
def about():
    if is_login():
        return render_template('login/login-about.html')
    return render_template('about.html')


@app.route('/setting')
def setting():
    if is_login():
        return render_template('login/user_setting.html')
    return redirect('/')


@app.route('/hot')
def hot():
    if is_login():
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                               page_size=15,
                               current_page=1,
                               url='hot/page')
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=1, page_size=15),
                               pagenation=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users)
    return render_template('hot_questions.html',
                           datas=get_hot_datas(page_num=1, page_size=15),
                           hot_users=db_users.Users().get_top5_users(),
                           hot_topics=db_topics.Topics().get_top5_topics())


@app.route('/wait-reply')
def wait_reply():
    if is_login():
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        pagenation = page_html(total_count=db_questions.Questions().get_wait_reply_questions_count(),
                               page_size=15,
                               current_page=1,
                               url='wait-reply/page')
        return render_template('login/login-wait_reply.html',
                               user=user,
                               datas=get_wait_reply_datas(page_num=1, page_size=15),
                               pagenation=pagenation,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('wait_reply.html')


@app.route('/people/<name>')
def people(name):
    if is_login():
        return render_template('login/login-person_detail.html')
    return render_template('person_detail.html')


@app.route('/setting/security')
def change_pass():
    if is_login():
        return render_template('login/change_pass.html')
    return redirect('/')
