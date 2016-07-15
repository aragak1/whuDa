# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, redirect, session
from utils import is_login, get_discover_datas, page_html, get_hot_datas
import whuDa.model.users as db_users
import whuDa.model.questions as db_questions
import whuDa.model.topics as db_topics
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


@app.route('/')
def index():
    if is_login():
        db_topics.Topics().get_topics_by_page(1,1)
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        pagenation = page_html(total_count=db_questions.Questions().get_questions_count(),
                               page_size=15,
                               current_page=1,
                               url='discover/page')
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=1, page_size=15),
                               pagenation=pagenation,
                               hot_topics=hot_topics,
                               hot_users=hot_users)
    return render_template('index.html')


@app.route('/discover/page/<int:page_num>')
def discover(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        pagenation = page_html(total_count=db_questions.Questions().get_questions_count(),
                               page_size=15,
                               current_page=page_num,
                               url='discover/page')
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=page_num, page_size=15),
                               pagenation=pagenation,
                               hot_topics=hot_topics,
                               hot_users=hot_users)
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


@app.route('/dynamic')
def dynamic():
    if is_login():
        return render_template('login/login-dynamic.html')
    return redirect('/')


@app.route('/topic')
def topic():
    if is_login():
        return render_template('login/login-topic.html')
    return render_template('topic.html')


@app.route('/topic/page/<int:page_num>')
def get_page_topic(page_num):
    if is_login():
        user = db_users.Users().get_uid_by_username(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=page_num,page_size=15)
        return render_template('login/login-topic.html',
                               user=user,
                               datas=datas)
    return render_template('topic.html')


@app.route('/topic/<topic_name>')
def topic_detail(topic_name):
    if is_login():
        return render_template('login/login-topic_detail.html')
    return render_template('topic_detail.html')


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


@app.route('/topic-recent-week')
def topic_recent_week():
    if is_login():
        return render_template('login/login-recent_week_topics.html')
    return render_template('recent_week_topics.html')


@app.route('/topic-recent-month')
def topic_recent_month():
    if is_login():
        return render_template('login/login-recent_month_topics.html')
    return render_template('recent_month_topics.html')


@app.route('/hot')
def hot():
    if is_login():
        hot_topics = db_topics.Topics().get_top5_topics()
        hot_users = db_users.Users().get_top5_users()
        user = db_users.Users().get_user(session['username'])
        pagenation = page_html(total_count=db_questions.Questions().get_questions_count(),
                               page_size=15,
                               current_page=1,
                               url='hot/page')
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=1, page_size=15),
                               pagenation=pagenation,
                               hot_topics=hot_topics,
                               hot_users=hot_users)
    return render_template('hot_questions.html')


@app.route('/wait-reply')
def wait_reply():
    if is_login():
        return render_template('login/login-wait_reply.html')
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


