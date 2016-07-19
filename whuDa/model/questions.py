# -*- coding: utf-8 -*-
from whuDa import db
from time import time
from sqlalchemy import desc, exists, not_
import whuDa.model.users as db_users
import whuDa.model.question_focus as db_question_focus
import whuDa.model.topic_focus as db_topic_focus

'''
    question_id int(11) unsigned not null auto_increment comment '问题ID',
    questioner_uid int(11) not null comment '提问者UID',
    title varchar(255) not null default '' comment '问题标题',
    content text not null comment '问题描述',
    publish_time int(10) not null comment '发布时间',
    update_time int(10) not null comment '最近修改时间',
    is_anonymous tinyint(1) not null default 0 comment '是否匿名',
    view_count int(10) not null default 0 comment '浏览次数',
    is_lock tinyint(1) not null default 0 comment '问题是否被锁定'
'''


class Questions(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True)
    questioner_uid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer, nullable=False)
    is_anonymous = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    is_lock = db.Column(db.Integer, nullable=False, default=0)

    # 添加一个新问题
    def publish(self, questioner_uid, title, content, is_anonymous):
        question = Questions(
            questioner_uid=questioner_uid,
            title=title,
            content=content,
            publish_time=time(),
            update_time=time(),
            is_anonymous=is_anonymous)
        db.session.add(question)
        db.session.flush()
        question_id = question.question_id
        db.session.commit()
        return question_id

    # 通过id获取问题
    def get_question_by_id(self, question_id):
        return db.session.query(Questions).filter(Questions.question_id == question_id).first()

    # 问题浏览数加一
    def add_question_view_count(self, question_id):
        db.session.query(Questions).filter_by(question_id=question_id).update({
            Questions.view_count: Questions.view_count + 1})
        db.session.commit()
        return True

    # 获取问题浏览数
    def get_question_view_count(self, question_id):
        return db.session.query(Questions, Questions.view_count).filter_by(question_id=question_id).first().view_count

    # 获取所有问题，按照发布时间排序
    def get_all_questions(self):
        return db.session.query(Questions).order_by(Questions.publish_time).all()

    # 获取问题总数
    def get_questions_count(self):
        return db.session.query(Questions).count()

    # 获取最新的问题，按照分页获取
    def get_questions_by_page(self, page_num, page_size):
        return db.session.query(Questions).order_by(desc(Questions.publish_time)).limit(page_size).offset((page_num-1)*page_size)

    # 获取热门问题，按照分页获取
    def get_hot_questions_by_page(self, page_num, page_size):
        return db.session.query(Questions).order_by(desc(Questions.view_count)).limit(page_size).offset((page_num-1)*page_size)

    # 获取发布者的uid
    def get_questioner_uid(self, question_id):
        return db.session.query(Questions.questioner_uid).filter_by(question_id=question_id).first().questioner_uid

    # 获取等待回复的问题的数量
    def get_wait_reply_questions_count(self):
        import whuDa.model.answers as db_answers
        return db.session.query(Questions).filter(not_(exists().where(db_answers.Answers.question_id == Questions.question_id))).count()

    # 获取等待回复问题，按照分页获取
    def get_wait_reply_questions_by_page(self, page_num, page_size):
        import whuDa.model.answers as db_answers
        return db.session.query(Questions).filter(not_(exists().where(db_answers.Answers.question_id == Questions.question_id))).limit(page_size).offset((page_num-1)*page_size)

    # 判断问题提是否其是七天内新增的
    def is_published_in_this_week(self, question_id):
        publish_time = Questions.query.filter_by(question_id=question_id).first().publish_time
        if time() - publish_time <= 604800:
            return True
        return False

    # 判断问题是否是一个月内新增的
    def is_published_in_this_month(self, question_id):
        publish_time = Questions.query.filter_by(question_id=question_id).first().publish_time
        if time() - publish_time <= 2592000:
            return True
        return False

    # 返回等待回复的问题
    def get_wait_reply_questions(self):
        import whuDa.model.answers as db_answers
        result = []
        questions = Questions.query.order_by(desc(Questions.publish_time)).all()
        for question in questions:
            if db_answers.Answers().question_is_answered(question.question_id):
                result.append(question)
        return result

    # 返回一个话题下所有的问题，按照发布时间排序
    def get_questions_by_topic_id(self, topic_id, desc_sort=True):
        import whuDa.model.topic_question as db_topic_question
        questions = []
        for question_id in db_topic_question.Topic_question().get_question_id_by_topic_id(topic_id):
            questions.append(self.get_question_by_id(question_id))
        if not desc_sort:
            questions.sort(cmp=lambda a, b: int(a.publish_time - b.publish_time))
        questions.sort(cmp=lambda a, b: int(b.publish_time - a.publish_time))
        return questions

    # 按照分页获取一个话题下的问题
    def get_questions_by_topic_id_and_page(self, topic_id, page_num, page_size, desc_sort=True):
        questions = self.get_questions_by_topic_id(topic_id, desc_sort)
        total_count = len(questions)
        start_index = (page_num-1)*page_size
        end_index = start_index + page_size
        if total_count > start_index:
            if total_count > end_index:
                return questions[start_index:end_index]
            return questions[start_index:]
        return []

    # 获取一个用户提出的所有问题
    def get_user_questions(self, username):
        return db.session.query(Questions).filter(Questions.questioner_uid == db_users.Users().
                                                  get_uid_by_username(username=username)).order_by(desc(Questions.publish_time)).all()

    # 获取一个问题的回复数
    def get_question_reply_count(self, question_id):
        import whuDa.model.answers as db_answers
        return db.session.query(db_answers.Answers).filter(db_answers.Answers.question_id == question_id).count()

    # 获取一个问题的关注数
    def get_question_focus_count(self, question_id):
        return db.session.query(db_question_focus.Question_focus).\
            filter(db_question_focus.Question_focus.question_id == question_id).count()

    # 获取一个用户提出的问题，并且按照时间由新到旧排序
    def get_questions_order_by_time(self, username):
        return db.session.query(Questions).filter(Questions.questioner_uid == db_users.Users().get_uid_by_username(username)).\
            order_by(desc(Questions.publish_time)).all()

    # 根据问题id获取问题的title
    def get_question_title_by_question_id(self, question_id):
        return db.session.query(Questions).filter_by(question_id=question_id).first().title

    def get_questions_order_by_time_by_uid(self, uid):
        return db.session.query(Questions).filter(
            Questions.questioner_uid == uid). \
            order_by(desc(Questions.publish_time)).all()

    # 按照分页获取一个用户提出的问题
    def get_questions_by_username_and_page(self, uid, page_num, page_size):
        questions = self.get_questions_order_by_time_by_uid(uid)
        total_count = len(questions)
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        if total_count > start_index:
            if total_count > end_index:
                return questions[start_index:end_index]
            return questions[start_index:]
        return []

    # 获取用户关注的话题（关注话题）下所有问题的id
    def get_question_ids_under_focus_topic(self, uid):
        return db_topic_focus.Topic_focus().get_question_ids_under_topic(uid)

    # 获取用户关注的问题（直接关注问题）id
    def get_user_focus_question_ids(self, uid):
        return db_question_focus.Question_focus().get_user_focus_question_ids(uid)

    # 获取动态列表需要读取的问题id
    def get_all_question_ids(self, uid):
        return self.get_question_ids_under_focus_topic(uid) + self.get_user_focus_question_ids(uid)

    # 获取用户关注的话题下所有的问题和关注的所有问题
    def get_dynamic_questions(self, uid):
        # question_id去重
        question_ids = list(set(self.get_all_question_ids(uid)))
        questions = []
        for question_id in question_ids:
            question = self.get_question_by_id(question_id)
            questions.append(question)
        return questions

    # 获取一个问题的10个相关问题,按照同一个话题下的来计算
    def get_ten_related_questions(self, question_id):
        import whuDa.model.topic_question as db_topic_question
        related_questions = []
        count = 0
        topics = db.session.query(db_topic_question.Topic_question).\
            filter(db_topic_question.Topic_question.question_id == question_id).all()
        break_flag = 0
        for topic in topics:
            if break_flag == 1:
                break
            questions = db.session.query(db_topic_question.Topic_question).\
                filter(db_topic_question.Topic_question.topic_id == topic.topic_id).\
                filter(db_topic_question.Topic_question.question_id != question_id).all()
            for question in questions:
                if count == 10:
                    break_flag = 1
                    break
                related_questions.append(db.session.query(Questions).
                                         filter(Questions.question_id == question.question_id).first())
                count += 1
        return related_questions

