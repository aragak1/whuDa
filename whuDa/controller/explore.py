# _*_ coding:utf8 _*_
import sys
import json
from time import time
from flask import render_template, redirect, session, request
import whuDa.model.department as db_department
import whuDa.model.questions as db_questions
import whuDa.model.topic_focus as db_topic_focus
import whuDa.model.topics as db_topics
import whuDa.model.users as db_users
import whuDa.model.notification as db_notification

import whuDa.model.question_focus as db_question_focus
from utils import is_login, get_discover_datas, page_html, get_hot_datas, get_wait_reply_datas, get_date
from whuDa import app
from utils import get_user_answer_datas, get_user_question_datas, get_user_focus_question_datas, get_user_latest_activity_datas
from utils import get_user_focus_questions_list_datas
from utils import get_notification_data
from utils import get_all_focus_data

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
    db_topics.Topics().get_topics_by_page(1, 1)
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=1,
                           url='discover/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        focus_topics = db_topic_focus.Topic_focus().get_user_focus_topics(user.uid)
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=1, page_size=15),
                               pagination=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users,
                               focus_topics=focus_topics)
    return render_template('index.html',
                           datas=get_discover_datas(page_num=1, page_size=15),
                           pagination=pagination,
                           hot_topics=hot_topics,
                           hot_users=hot_users)


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
                               pagination=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users,
                               focus_topics=focus_topics)
    return render_template('index.html',
                           datas=get_discover_datas(page_num=page_num, page_size=15),
                           pagination=pagination,
                           hot_topics=hot_topics,
                           hot_users=hot_users)


@app.route('/hot/page/<int:page_num>')
def hot_page(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=page_num,
                           url='hot/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=page_num, page_size=15),
                               pagination=pagination,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('hot_questions.html',
                           datas=get_hot_datas(page_num=page_num, page_size=15),
                           pagination=pagination,
                           hot_users=hot_users,
                           hot_topics=hot_topics)


@app.route('/wait-reply/page/<int:page_num>')
def wait_reply_page(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_wait_reply_questions_count(),
                           page_size=15,
                           current_page=page_num,
                           url='wait-reply/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-wait_reply.html',
                               user=user,
                               datas=get_wait_reply_datas(page_num=page_num, page_size=15),
                               pagination=pagination,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('wait_reply.html',
                           datas=get_wait_reply_datas(page_num=page_num, page_size=15),
                           pagination=pagination,
                           hot_users=hot_users,
                           hot_topics=hot_topics)


@app.route('/dynamic')
def dynamic():
    if is_login():
        return render_template('login/login-dynamic.html')
    return redirect('/')


@app.route('/all_focus')
def question_focus():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        uid=user.uid
        question_focus=db_question_focus.Question_focus().get_user_focus_questions(session['username'])

        return render_template('login/all_focus.html',
                               user=user)
    else:
        return redirect('/')


@app.route('/all_focus.json',methods=['POST'])
def more_question_focus():
    if request.method == 'POST':
        page_num = int(request.form.get('page_num'))
        datas =get_all_focus_data(session['username'])
        if len(datas['all_focus']) > 5 * (page_num + 1):
            datas['all_focus'] = datas['all_focus'][5 * page_num:5 * (page_num + 1)]
            more = 1
        else:
            datas['all_focus'] = datas['all_focus'][5 * page_num:]
            more = 0
        page_num = page_num + 1
        datas['more'] = more
        datas['page_num'] = page_num
        return json.dumps(datas, ensure_ascii=False)
    else:
        return redirect('/')



@app.route('/notifications', methods=['GET', 'POST'])
def show_notifications():
    if request.method == 'GET' and is_login():
        uid=db_users.Users().get_uid_by_username(session['username'])
        datas=get_notification_data(uid)
        more=0
        page=1
        unread=datas['unread']


        if len(datas['notifications'])>5:
            notifications=datas['notifications'][0:5]
            more=1
        return render_template('login/notifications.html',
                               unread=unread,
                               notifications=notifications,
                               more=more,
                               page=page)
    elif request.method == 'POST':
        option=request.form.get('option')
        if option=='has_read':
            id=request.form.get('notification_id')
            return db_notification.Notification().has_read(id)
        elif option=='delete':
            id=request.form.get('notification_id')
            uid = db_users.Users().get_uid_by_username(session['username'])
            return db_notification.Notification().delete(id,uid)
        elif option=='read_all':
            db_notification.Notification().read_all()
            pass
    return redirect('/')


@app.route('/notifications.json',methods=['POST','GET'])
def get_more_notifications():
    if request.method=='POST':

        page_num=int(request.form.get('page_num'))

        uid = db_users.Users().get_uid_by_username(session['username'])
        datas = get_notification_data(uid)
        if len(datas['notifications']) > 5 * (page_num + 1):
            datas['notifications'] = datas['notifications'][5*page_num:5 * (page_num + 1)]
            more = 1
        else:
            datas['notifications']=datas['notifications'][5*page_num:]
            more = 0
        page_num = page_num + 1
        datas['more']=more
        datas['page_num']=page_num
        return json.dumps(datas, ensure_ascii=False)
    else:
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
        dates = {
            'year': [y for y in range(1900, 1+get_date(time())['year'])],
            'month': [m for m in range(1, 13)],
            'day': [d for d in range(1, 32)]}
        birthday = db_users.Users().get_birthday_dict(db_users.Users().get_uid_by_username(session['username']))
        departments = db_department.Department().get_all_department()
        user = db_users.Users().get_user(session['username'])
        return render_template('login/user_setting.html',
                               user=user,
                               departments=departments,
                               dates=dates,
                               birthday=birthday)
    return redirect('/')


@app.route('/setting/security')
def change_pass():
    if is_login():
        return render_template('login/change_pass.html')
    return redirect('/')


@app.route('/hot')
def hot():
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=1,
                           url='hot/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=1, page_size=15),
                               pagination=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users)
    return render_template('hot_questions.html',
                           datas=get_hot_datas(page_num=1, page_size=15),
                           pagination=pagination,
                           hot_topics=hot_topics,
                           hot_users=hot_users)


@app.route('/wait-reply')
def wait_reply():
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_wait_reply_questions_count(),
                           page_size=15,
                           current_page=1,
                           url='wait-reply/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-wait_reply.html',
                               user=user,
                               datas=get_wait_reply_datas(page_num=1, page_size=15),
                               pagination=pagination,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('wait_reply.html',
                           datas=get_wait_reply_datas(page_num=1, page_size=15),
                           pagination=pagination,
                           hot_users=hot_users,
                           hot_topics=hot_topics)


# 需要一个user，一个people，5条回复，5条提问，5个动态，关注话题，关注的问题
# question的reply_count手动计算
# question的focus_count手动计算
# 动态的所有数据都要手动计算
# 关注的话题涉及topic_focus和topics的连接查询
@app.route('/people/<name>')
def people(name):
    people = db_users.Users().get_user(username=name)
    temp_answer_datas = get_user_answer_datas(name)
    temp_question_datas = get_user_question_datas(name)
    temp_focus_topic_datas = db_topic_focus.Topic_focus().get_user_focus_topics(db_users.Users().get_uid_by_username(name))
    temp_focus_question_datas = get_user_focus_question_datas(name)
    temp_latest_activity_datas = get_user_latest_activity_datas(username=name)
    temp_question_list_datas = temp_question_datas
    temp_answer_list_datas = temp_answer_datas
    focus_question_list_datas = get_user_focus_questions_list_datas(people.uid)
    if len(temp_answer_datas) > 5:
        answer_datas = temp_answer_datas[0:5]
    else:
        answer_datas = temp_answer_datas
    if len(temp_question_datas) > 5:
        question_datas = temp_question_datas[0:5]
    else:
        question_datas = temp_question_datas
    if len(temp_focus_topic_datas) > 5:
        focus_topic_datas = temp_focus_topic_datas[0:5]
    else:
        focus_topic_datas = temp_focus_topic_datas
    if len(temp_focus_question_datas) > 5:
        focus_question_datas = temp_focus_question_datas[0:5]
    else:
        focus_question_datas = temp_focus_question_datas
    if len(temp_latest_activity_datas) > 5:
        latest_activity_datas = temp_latest_activity_datas[0:5]
    else:
        latest_activity_datas = temp_latest_activity_datas
    if len(temp_question_list_datas) > 15:
        question_list_datas = temp_question_list_datas[0:15]
    else:
        question_list_datas = temp_question_list_datas
    if len(temp_answer_list_datas) > 15:
        answer_list_datas = temp_answer_list_datas[0:15]
    else:
        answer_list_datas = temp_answer_list_datas
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-person_detail.html',
                               user=user,
                               people=people,
                               answer_datas=answer_datas,
                               question_datas=question_datas,
                               latest_activity_datas=latest_activity_datas,
                               focus_topic_datas=focus_topic_datas,
                               focus_question_datas=focus_question_datas,
                               question_focus_count=db_question_focus.Question_focus().get_user_focus_question_count(name),
                               question_list_datas=question_list_datas,
                               answer_list_datas=answer_list_datas,
                               focus_question_list_datas=focus_question_list_datas)
    return render_template('person_detail.html',
                           people=people,
                           answer_datas=answer_datas,
                           question_datas=question_datas,
                           latest_activity_datas=latest_activity_datas,
                           focus_topic_datas=focus_topic_datas,
                           focus_question_datas=focus_question_datas,
                           question_focus_count=db_question_focus.Question_focus().get_user_focus_question_count(name),
                           question_list_datas=question_list_datas,
                           answer_list_datas=answer_list_datas,
                           focus_question_list_datas=focus_question_list_datas)


