# _*_ coding:utf8 _*_
from whuDa import app
from flask import request, redirect, render_template, session
from utils import is_login
import whuDa.model.questions as db_questions
import whuDa.model.topic_question as db_topic_questions
import whuDa.model.topics as db_topics
import whuDa.model.question_focus as db_question_focus
import whuDa.model.users as db_users
import whuDa.model.answers as db_answers
from utils import get_past_time

'''
    发布一个问题需要进行的操作：
    1.添加一个问题，
    2.发布者关注该问题，
    3.发布者的问题数加一，
    4.添加问题所属的话题记录
'''

'''
    添加一个回复需要进行的操作：
    1.添加一个回复
    2.回复者是否关注该回复，
    3.回复者答案数加一，
    4.给提问者发送通知，（未完成）
'''


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/publish.html', user=user)
    return redirect('/')


@app.route('/publish/<int:question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    if is_login():
        if request.method == 'POST':
            return 'success'
        else:
            return 'error'
    return redirect('/')


@app.route('/publish/question', methods=['POST'])
def publish_question():
    if is_login():
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            topics = request.form.getlist('topics[]')
            is_anonymous = int(request.form.get('anonymous'))
            if title == '':
                return 'empty_title'
            if not topics:
                return 'empty_topics'

            uid = db_users.Users().get_uid_by_username(session['username'])

            # 在question表中插入问题
            question_id = db_questions.Questions().publish(
                questioner_uid=uid,
                title=title,
                content=content,
                is_anonymous=is_anonymous)

            # 把问题所属的话题加入表中
            for topic in topics:
                topic_id = db_topics.Topics().get_topic_id_by_name(topic)
                db_topic_questions.Topic_question().add_to_topic(
                    question_id=question_id,
                    topic_id=topic_id)

            # 用户关注该问题
            db_question_focus.Question_focus().add_focus_question(uid=uid, question_id=question_id, cnt=1)

            # 用户问题数加一
            db_users.Users().add_question_count(session['username'])
            return str(question_id)
    return redirect('/')


@app.route('/question/<int:id>')
def question(id):
    related_questions = db_questions.Questions().get_ten_related_questions(id)
    db_questions.Questions().add_question_view_count(id)
    question = db_questions.Questions().get_question_by_id(id)
    publish_time = get_past_time(question.publish_time)
    answer_count = db_answers.Answers().get_answer_count(question.question_id)
    questioner = db_users.Users().get_user_by_id(uid=question.questioner_uid)
    question_focus_cnt = db_question_focus.Question_focus().get_question_foucs_count(id)
    answers = db_answers.Answers().get_all_answer(id)
    answer_users = []
    for answer in answers:
        answer_users.append(db_users.Users().get_user_by_id(answer.answer_uid))
    # 合并answers和answer_users
    answers_and_users = []
    for i in range(len(answers)):
        answer_and_user = {
            'uid': answers[i].answer_uid,
            'content': answers[i].content,
            'username': answer_users[i].username,
            'avatar_url': answer_users[i].avatar_url,
            'introduction': answer_users[i].introduction}
        answers_and_users.append(answer_and_user)
    if question:
        topic_ids = db_topic_questions.Topic_question().get_topics_by_id(question_id=question.question_id)
        topics = []
        for topic_id in topic_ids:
            temp_dict = {'topic_id': topic_id, 'name': db_topics.Topics().get_topic_name_by_id(topic_id)}
            topics.append(temp_dict)
        if is_login():
            user = db_users.Users().get_user(session['username'])
            question_focused = db_question_focus.Question_focus().question_focused(id, uid=user.uid)
            if len(related_questions) > 5:
                five_related_questions = related_questions[0:5]
            else:
                five_related_questions = related_questions
            return render_template('login/login-question_detail.html',
                                   question=question,
                                   topics=topics,
                                   user=user,
                                   question_focus_cnt=question_focus_cnt,
                                   questioner=questioner,
                                   answers_and_users=answers_and_users,
                                   publish_time=publish_time,
                                   answer_count=answer_count,
                                   related_questions=five_related_questions,
                                   question_focused=question_focused)
        return render_template('question_detail.html',
                               question=question,
                               topics=topics,
                               question_focus_cnt=question_focus_cnt,
                               questioner=questioner,
                               answers_and_users=answers_and_users,
                               publish_time=publish_time,
                               answer_count=answer_count,
                               related_questions=related_questions)
    return '没有这个问题'


@app.route('/question/answer', methods=['POST'])
def answer():
    if is_login():
        question_id = int(request.form.get('question_id'))
        answer_content = request.form.get('answer_content')
        is_anonymous = int(request.form.get('is_anonymous'))
        focus_question = int(request.form.get('focus_question'))
        answer_user = db_users.Users().get_user(session['username'])
        # 判断是否已经回答过该问题
        if db_answers.Answers().answered(uid=answer_user.uid, question_id=question_id):
            return 'answered'
        if answer_content == '':
            return 'empty_content'
        # 添加答案
        db_answers.Answers().add_answer(question_id=question_id,
                                        answer_uid=answer_user.uid,
                                        content=answer_content,
                                        is_anonymous=is_anonymous)
        # 答复者是否关注该问题
        if focus_question and not db_question_focus.Question_focus().question_focused(uid=answer_user.uid,
                                                                                      question_id=question_id):
            focus_count = db_question_focus.Question_focus().get_question_foucs_count(question_id=question_id)
            db_question_focus.Question_focus().add_focus_question(uid=answer_user.uid,
                                                                  question_id=question_id,
                                                                  cnt=focus_count + 1)

        # 回答者答复数加一
        db_users.Users().add_answer_count(session['username'])
        return 'success'
    return 'error'


@app.route('/question/cancel_focus', methods=['POST'])
def cancel_question_focus():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        question_id = request.form.get('question_id')
        db_question_focus.Question_focus().question_cancel_focus(question_id, user.uid)
        return 'success'
    return 'error'


@app.route('/question/add_focus', methods=['POST'])
def add_question_focus():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        question_id = request.form.get('question_id')
        db_question_focus.Question_focus().add_focus_question(user.uid, question_id=question_id, cnt=0)
        return 'success'
    return 'error'
