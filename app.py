import requests
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_admin import Admin
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from flask_cors import CORS
import logging
from logging import FileHandler, Formatter

app = Flask(__name__)

DATABASE_URI = 'sqlite:///database.db'
engine = create_engine(DATABASE_URI)
app.secret_key = 'dorqi'
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
CORS(app)
app.logger.setLevel(logging.DEBUG)
file_handler = FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    coins = Column(Integer, default=0)
    has_clicker_bot = Column(Boolean, default=False)
    multitap_level = Column(Integer, default=0)
    recharge_level = Column(Integer, default=0)
    referral_link = Column(String(255))
    referred_count = Column(Integer, default=0)
    wallet_address = Column(String(255))
    game_2048_score = Column(Integer, default=0)
    total_contributed_to_referrer = Column(Integer, default=0)
    cinema_tasks = relationship('CinemaTask', back_populates='user')
    live_task = relationship('LiveTask', back_populates='user', uselist=False)
    channel_tasks = relationship('ChannelTask', back_populates='user')
    referral_task = relationship('ReferralTask', back_populates='user', uselist=False)
    referred_users = relationship('ReferredUser', back_populates='referrer')
    tasks = relationship('UserTask', back_populates='user')
    calculation_history = relationship('ReferralCalculationHistory', back_populates='user')
class UserTask(Base):
    __tablename__ = 'user_tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cinema_task_id = Column(Integer, ForeignKey('cinema_tasks.id'), nullable=True)
    live_task_id = Column(Integer, ForeignKey('live_tasks.id'), nullable=True)
    channel_task_id = Column(Integer, ForeignKey('channel_tasks.id'), nullable=True)
    referral_task_id = Column(Integer, ForeignKey('referral_tasks.id'), nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='tasks')
    cinema_task = relationship('CinemaTask')
    live_task = relationship('LiveTask')
    channel_task = relationship('ChannelTask')
    referral_task = relationship('ReferralTask')
    
class ReferralCalculationHistory(Base):
    __tablename__ = 'referral_calculation_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    referred_user_id = Column(Integer, ForeignKey('referred_users.id'))
    calculated_at = Column(DateTime, default=datetime.utcnow)
    calculated_coins = Column(Integer, nullable=False)

    user = relationship('User', back_populates='calculation_history')
    referred_user = relationship('ReferredUser')
class ReferredUser(Base):
    __tablename__ = 'referred_users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    coins = Column(Integer, default=0)
    referrer_id = Column(Integer, ForeignKey('users.id'))
    referrer = relationship('User', back_populates='referred_users')

class Advertisement(Base):
    __tablename__ = 'advertisements'
    
    id = Column(Integer, primary_key=True)
    link = Column(String(255), nullable=False)
    text = Column(String(255), nullable=False)
    is_english = Column(Boolean, default=True)

class CinemaTask(Base):
    __tablename__ = 'cinema_tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    youtube_link = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    slug = Column(String(100), unique=True, nullable=False)
    social = Column(String(50), nullable=False)
    user = relationship('User', back_populates='cinema_tasks')


class LiveTask(Base):
    __tablename__ = 'live_tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    max_claims = Column(Integer, nullable=False)
    current_claims = Column(Integer, default=0)
    coins_reward = Column(Integer, nullable=False)
    social = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='live_task')

class ChannelTask(Base):
    __tablename__ = 'channel_tasks'
    
    id = Column(Integer, primary_key=True)
    channel_name = Column(String(100), nullable=False)
    channel_link = Column(String(255), nullable=False)
    coins_reward = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    social = Column(String(50), nullable=False)
    user = relationship('User', back_populates='channel_tasks')
class LiveTaskClaim(Base):
    __tablename__ = 'live_task_claims'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    live_task_id = Column(Integer, ForeignKey('live_tasks.id'))
    claimed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User')
    live_task = relationship('LiveTask')

class ReferralTask(Base):
    __tablename__ = 'referral_tasks'
    
    id = Column(Integer, primary_key=True)
    required_referrals = Column(Integer, nullable=False)
    coins_reward = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    social = Column(String(50), nullable=False)
    user = relationship('User', back_populates='referral_task')

class LiveAvailability(Base):
    __tablename__ = 'live_availability'
    
    id = Column(Integer, primary_key=True)
    have_live = Column(Boolean, default=False)

class UserTaskAssociation(Base):
    __tablename__ = 'user_task_associations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, nullable=False)  # This will store the ID of the task
    task_type = Column(String(50), nullable=False)  # This will store the type of the task (e.g., "CinemaTask", "LiveTask")
    completed = Column(Boolean, default=False)
class Reset2048ScoresView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            session.query(User).update({User.game_2048_score: 0})
            session.commit()
            return self.render('admin/2048_reset_success.html')
        return self.render('admin/reset_2048_scores.html')


class ClaimedUsersView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/claimed_users.html')

    @expose('/<string:code>')
    def claimed_users(self, code):
        task = session.query(LiveTask).filter_by(code=code).first()
        if task:
            claimed_users = session.query(LiveTaskClaim).filter_by(live_task_id=task.id).all()
            claimed_users_list = [{'username': claim.user.username, 'wallet_address': claim.user.wallet_address} for claim in claimed_users]
            return self.render('admin/claimed_users.html', claimed_users=claimed_users_list)
        return 'Task not found', 404


Base.metadata.create_all(engine)

admin = Admin(app, name='AirdropBot Admin', template_mode='bootstrap3')

admin.add_view(ModelView(User, session))
admin.add_view(ModelView(UserTask, session))
admin.add_view(ModelView(ReferralCalculationHistory, session))
admin.add_view(ModelView(ReferredUser, session))
admin.add_view(ModelView(Advertisement, session))
admin.add_view(ModelView(CinemaTask, session))
admin.add_view(ModelView(LiveTask, session))
admin.add_view(ModelView(ChannelTask, session))
admin.add_view(ModelView(LiveTaskClaim, session))
admin.add_view(ModelView(ReferralTask, session))
admin.add_view(ModelView(LiveAvailability, session))
admin.add_view(ModelView(UserTaskAssociation, session))
admin.add_view(Reset2048ScoresView(name='ریست امتیازات 2048', endpoint='reset_2048_scores'))
admin.add_view(ClaimedUsersView(name='Claimed Users'))
admin.add_view(ClaimedUsersView(name='Claimed Users', endpoint='claimedusers'))




def calculate_referral_bonus(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return
    
    total_bonus = 0
    now = datetime.utcnow()

    for referred_user in user.referred_users:
        last_24_hours = now - timedelta(hours=24)
        # چک کردن که آیا قبلاً این زیرمجموعه برای این کاربر در 24 ساعت گذشته محاسبه شده است یا نه
        already_calculated = session.query(ReferralCalculationHistory).filter(
            ReferralCalculationHistory.user_id == user_id,
            ReferralCalculationHistory.referred_user_id == referred_user.id,
            ReferralCalculationHistory.calculated_at >= last_24_hours
        ).first()

        if not already_calculated:
            bonus = int(0.10 * referred_user.coins)
            total_bonus += bonus

            # ذخیره تاریخچه محاسبه
            new_calculation = ReferralCalculationHistory(
                user_id=user_id,
                referred_user_id=referred_user.id,
                calculated_coins=bonus,
                calculated_at=now
            )
            session.add(new_calculation)
    
    user.coins += total_bonus
    session.commit()

@app.route('/api/live/availability', methods=['GET', 'POST'])
def live_availability():
    live_status = session.query(LiveAvailability).first()
    if request.method == 'GET':
        return jsonify({'have_live': live_status.have_live}) if live_status else jsonify({'have_live': False})
    
    if request.method == 'POST':
        data = request.json
        if live_status:
            live_status.have_live = data.get('have_live', live_status.have_live)
        else:
            live_status = LiveAvailability(have_live=data.get('have_live', False))
            session.add(live_status)
        session.commit()
        return jsonify({'message': 'Live availability updated successfully'}), 200

@app.route('/api/cinema-tasks', methods=['POST'])
def add_cinema_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    youtube_link = data.get('youtube_link')
    code = data.get('code')
    slug = data.get('slug')
    social = data.get('social')
    
    if title and description and youtube_link and code and slug and social:
        task = CinemaTask(
            title=title,
            description=description,
            youtube_link=youtube_link,
            code=code,
            slug=slug,
            social=social
        )
        session.add(task)
        session.commit()
        return jsonify({'message': 'Cinema task added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/cinema-tasks/<string:slug>', methods=['GET'])
def get_cinema_task(slug):
    task = session.query(CinemaTask).filter_by(slug=slug).first()
    if task:
        task_data = {
            'title': task.title,
            'id': task.id,
            'description': task.description,
            'youtube_link': task.youtube_link,
            'code': task.code,
            'social': task.social
        }
        return jsonify(task_data)
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/api/live-tasks', methods=['POST'])
def add_live_task():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    code = data.get('code')
    max_claims = data.get('max_claims')
    coins_reward = data.get('coins_reward')
    social = data.get('social')
    
    if title and description and code and max_claims and coins_reward and social:
        task = LiveTask(
            title=title,
            description=description,
            code=code,
            max_claims=max_claims,
            coins_reward=coins_reward,
            social=social
        )
        session.add(task)
        session.commit()
        return jsonify({'message': 'Live task added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400
@app.route('/api/live-task/<string:code>/claim', methods=['POST'])
def claim_live_task(code):
    task = session.query(LiveTask).filter_by(code=code).first()
    if task:
        if task.current_claims < task.max_claims:
            task.current_claims += 1
            user_id = request.json.get('user_id')
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                # ذخیره‌سازی کلیم
                live_task_claim = LiveTaskClaim(user_id=user_id, live_task_id=task.id)
                session.add(live_task_claim)
                
                # اضافه کردن سکه به کاربر
              
                session.commit()
                return jsonify({'message': 'Task claimed successfully'}), 200
        else:
            return jsonify({'error': 'Maximum number of claims reached'}), 403
    return jsonify({'error': 'Task not found or already claimed'}), 404

@app.route('/api/live-task/<string:code>/claimed-users', methods=['GET'])
def get_claimed_users(code):
    task = session.query(LiveTask).filter_by(code=code).first()
    if task:
        claimed_users = session.query(LiveTaskClaim).filter_by(live_task_id=task.id).all()
        claimed_users_list = [{'username': claim.user.username, 'wallet_address': claim.user.wallet_address} for claim in claimed_users]
        return jsonify(claimed_users_list), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/channel-tasks', methods=['POST'])
def add_channel_task():
    data = request.json
    channel_name = data.get('channel_name')
    channel_link = data.get('channel_link')
    coins_reward = data.get('coins_reward')
    social = data.get('social')
    
    if channel_name and channel_link and coins_reward and social:
        task = ChannelTask(
            channel_name=channel_name,
            channel_link=channel_link,
            coins_reward=coins_reward,
            social=social
        )
        session.add(task)
        session.commit()
        return jsonify({'message': 'Channel task added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/referral-tasks', methods=['POST'])
def add_referral_task():
    data = request.json
    required_referrals = data.get('required_referrals')
    coins_reward = data.get('coins_reward')
    social = data.get('social')
    
    if required_referrals and coins_reward and social:
        task = ReferralTask(
            required_referrals=required_referrals,
            coins_reward=coins_reward,
            social=social
        )
        session.add(task)
        session.commit()
        return jsonify({'message': 'Referral task added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        referred_users = session.query(ReferredUser).filter_by(referrer_id=user.id).all()
        
        # دریافت تسک‌های_PENDING_
        # بازیابی تسک‌های سینما که کاربر انجام نداده است
        cinema_tasks = session.query(CinemaTask).outerjoin(UserTask, CinemaTask.id == UserTask.cinema_task_id).filter(
            (UserTask.user_id != user_id) | (UserTask.user_id.is_(None))
        ).all()

        
        channel_tasks = session.query(ChannelTask).filter(
            ChannelTask.user_id.is_(None) | (ChannelTask.user_id != user_id)
        ).all()
        
        referral_tasks = session.query(ReferralTask).filter(
            ReferralTask.user_id.is_(None) | (ReferralTask.user_id != user_id)
        ).all()

        # دریافت 10 امتیاز برتر در بازی 2048 که بیشتر از 0 باشند
        top_scores = session.query(User).filter(User.game_2048_score > 0).order_by(User.game_2048_score.desc()).limit(10).all()
        top_scores_list = [{'id': user.id, 'username': user.username, 'score': user.game_2048_score} for user in top_scores]

        # دریافت 10 کاربر برتر از نظر تعداد معرفی که بیشتر از 0 باشد
        top_referrals = session.query(User).filter(User.referred_count > 0).order_by(User.referred_count.desc()).limit(10).all()
        top_referrals_list = [{'id': user.id, 'username': user.username, 'referred_count': user.referred_count} for user in top_referrals]

        # دریافت 10 کاربر برتر از نظر تعداد سکه‌ها که بیشتر از 0 باشد
        top_coins = session.query(User).filter(User.coins > 0).order_by(User.coins.desc()).limit(10).all()
        top_coins_list = [{'id': user.id, 'username': user.username, 'coins': user.coins} for user in top_coins]

        # دریافت اطلاعات دسترسی سرویس‌ها
        live_status = session.query(LiveAvailability).first()
        service_availability = {'have_live': live_status.have_live} if live_status else {'have_live': False}

        user_data = {
            'id': user.id,
            'username': user.username,
            'coins': user.coins,
            'has_clicker_bot': user.has_clicker_bot,
            'referral_link': user.referral_link,
            'referred_count': user.referred_count,
            'wallet_address': user.wallet_address,
            'game_2048_score': user.game_2048_score,
            'total_contributed_to_referrer': user.total_contributed_to_referrer,
            'referred_users': [
                {
                    'username': u.username,
                    'coins': sum([h.calculated_coins for h in session.query(ReferralCalculationHistory).filter_by(referred_user_id=u.id).all()])
                } for u in referred_users
            ],
            'pending_tasks': {
                'cinema_tasks': [
                    {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'youtube_link': task.youtube_link,
                        'code': task.code,
                        'slug': task.slug,
                        'social': task.social
                    }
                    for task in cinema_tasks
                ],
                'channel_tasks': [
                    {
                        'id': task.id,
                        'channel_name': task.channel_name,
                        'channel_link': task.channel_link,
                        'coins_reward': task.coins_reward,
                        'social': task.social
                    }
                    for task in channel_tasks
                ],
                'referral_tasks': [
                    {
                        'id': task.id,
                        'required_referrals': task.required_referrals,
                        'coins_reward': task.coins_reward,
                        'social': task.social
                    }
                    for task in referral_tasks
                ],
            },
            'top_users': {
                'top_2048_scores': top_scores_list,
                'top_referrals': top_referrals_list,
                'top_coins': top_coins_list
            },
            'service_availability': service_availability  # اضافه کردن اطلاعات دسترسی به پاسخ
        }
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.json
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.wallet_address = data.get('wallet_address', user.wallet_address)
        user.game_2048_score = data.get('game_2048_score', user.game_2048_score)
        user.coins = data.get('coins', user.coins)
        user.has_clicker_bot = data.get('has_clicker_bot', user.has_clicker_bot)
        user.multitap_level = data.get('multitap_level', user.multitap_level)
        user.recharge_level = data.get('recharge_level', user.recharge_level)
        session.commit()
        
        # بازگرداندن مقدار جدید رکورد تغییر یافته
        updated_user = {
            'id': user.id,
            'wallet_address': user.wallet_address,
            'game_2048_score': user.game_2048_score,
            'coins': user.coins,
            'has_clicker_bot': user.has_clicker_bot,
            'multitap_level': user.multitap_level,
            'recharge_level': user.recharge_level
        }
        
        return jsonify({'message': 'User updated successfully', 'user': updated_user}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/ads', methods=['POST'])
def add_ad():
    data = request.json
    link = data.get('link')
    text = data.get('text')
    is_english = data.get('is_english', True)

    if link and text:
        ad = Advertisement(link=link, text=text, is_english=is_english)
        session.add(ad)
        session.commit()
        return jsonify({'message': 'Advertisement added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/ads', methods=['GET'])
def get_ads():
    ads = session.query(Advertisement).all()
    ads_list = [{'id': ad.id, 'link': ad.link, 'text': ad.text, 'is_english': ad.is_english} for ad in ads]
    return jsonify(ads_list)


@app.route('/api/cinema-tasks', methods=['GET'])
def get_cinema_tasks():
    tasks = session.query(CinemaTask).filter_by(user_id=None).all()
    tasks_list = [{'slug': task.slug, 'title': task.title, 'social': task.social} for task in tasks]
    return jsonify(tasks_list)

@app.route('/api/pending-tasks/<int:user_id>', methods=['GET'])
def get_pending_tasks(user_id):
    # بازیابی تسک‌های سینما که کاربر انجام نداده است
    # بازیابی تسک‌های سینما که کاربر انجام نداده است
    cinema_tasks = session.query(CinemaTask).outerjoin(UserTask, CinemaTask.id == UserTask.cinema_task_id).filter(
         (UserTask.user_id != user_id) | (UserTask.user_id.is_(None))
    ).all()

    
    # بازیابی تسک‌های کانال که کاربر انجام نداده است
    channel_tasks = session.query(ChannelTask).filter(
        ChannelTask.user_id.is_(None) | (ChannelTask.user_id != user_id)
    ).all()
    
    # بازیابی تسک‌های رفرال که کاربر انجام نداده است
    referral_tasks = session.query(ReferralTask).filter(
        ReferralTask.user_id.is_(None) | (ReferralTask.user_id != user_id)
    ).all()

    tasks = {
        'cinema_tasks': [
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'youtube_link': task.youtube_link,
                'code': task.code,
                'slug': task.slug,
                'social': task.social
            }
            for task in cinema_tasks
        ],
        'channel_tasks': [
            {
                'id': task.id,
                'channel_name': task.channel_name,
                'channel_link': task.channel_link,
                'coins_reward': task.coins_reward,
                'social': task.social
            }
            for task in channel_tasks
        ],
        'referral_tasks': [
            {
                'id': task.id,
                'required_referrals': task.required_referrals,
                'coins_reward': task.coins_reward,
                'social': task.social
            }
            for task in referral_tasks
        ],
    }

    return jsonify(tasks)

@app.route('/api/2048/reset-scores', methods=['POST'])
def reset_2048_scores():
    session.query(User).update({User.game_2048_score: 0})
    session.commit()
    return jsonify({'message': 'All 2048 scores have been reset to 0'}), 200
@app.route('/api/top-users', methods=['GET'])
def get_top_users():
    # دریافت 10 امتیاز برتر در بازی 2048 که بیشتر از 0 باشند
    top_scores = session.query(User).filter(User.game_2048_score > 0).order_by(User.game_2048_score.desc()).limit(10).all()
    top_scores_list = [{'id': user.id, 'username': user.username, 'score': user.game_2048_score} for user in top_scores]

    # دریافت 10 کاربر برتر از نظر تعداد معرفی که بیشتر از 0 باشد
    top_referrals = session.query(User).filter(User.referred_count > 0).order_by(User.referred_count.desc()).limit(10).all()
    top_referrals_list = [{'id': user.id, 'username': user.username, 'referred_count': user.referred_count} for user in top_referrals]

    # دریافت 10 کاربر برتر از نظر تعداد سکه‌ها که بیشتر از 0 باشد
    top_coins = session.query(User).filter(User.coins > 0).order_by(User.coins.desc()).limit(10).all()
    top_coins_list = [{'id': user.id, 'username': user.username, 'coins': user.coins} for user in top_coins]

    # ترکیب تمامی نتایج در یک دیکشنری
    result = {
        'top_2048_scores': top_scores_list,
        'top_referrals': top_referrals_list,
        'top_coins': top_coins_list
    }

    return jsonify(result)
@app.route('/api/cinema-task/<int:task_id>/claim', methods=['POST'])
def claim_cinema_task(task_id):
    user_id = request.json.get('user_id')
    user = session.query(User).filter_by(id=user_id).first()
    task = session.query(CinemaTask).filter_by(id=task_id).first()

    app.logger.debug(f'Claim request for Cinema Task - User ID: {user_id}, Task ID: {task_id}')
    
    if not user or not task:
        app.logger.error('User or task not found')
        return jsonify({'error': 'User or task not found'}), 404

    claimed_task = session.query(UserTask).filter_by(user_id=user.id, cinema_task_id=task.id).first()
    if claimed_task:
        app.logger.warning('Task already claimed by user')
        return jsonify({'error': 'Task already claimed'}), 403

    user_task = UserTask(user_id=user.id, cinema_task_id=task.id)
    session.add(user_task)
    session.commit()

    app.logger.info(f'Cinema task claimed successfully by User ID: {user_id}, Task ID: {task.id}')
    return jsonify({'message': 'Cinema task claimed successfully'}), 200

    user_id = request.json.get('user_id')
    user = session.query(User).filter_by(id=user_id).first()

    # پیدا کردن تسک بر اساس slug
    task = session.query(CinemaTask).filter_by(slug=slug).first()

    # لاگ اطلاعات ورودی
    app.logger.debug(f'Claim request for Cinema Task - User ID: {user_id}, Task Slug: {slug}')
    
    if not user or not task:
        app.logger.error('User or task not found')
        return jsonify({'error': 'User or task not found'}), 404

    # بررسی این که آیا کاربر قبلاً تسک را کلایم کرده است
    claimed_task = session.query(UserTask).filter_by(user_id=user.id, cinema_task_id=task.id).first()
    if claimed_task:
        app.logger.warning('Task already claimed by user')
        return jsonify({'error': 'Task already claimed'}), 403

    # اضافه کردن تسک جدید
    user_task = UserTask(user_id=user.id, cinema_task_id=task.id)
    session.add(user_task)
    session.commit()

    app.logger.info(f'Cinema task claimed successfully by User ID: {user_id}, Task ID: {task.id}')
    return jsonify({'message': 'Cinema task claimed successfully'}), 200

    user_id = request.json.get('user_id')
    user = session.query(User).filter_by(id=user_id).first()
    task = session.query(CinemaTask).filter_by(slug=slug).first()

    if not user or not task:
        return jsonify({'error': 'User or task not found'}), 404

    # Check if the user already claimed the task
    claimed_task = session.query(UserTask).filter_by(user_id=user.id, cinema_task_id=task.id).first()
    if claimed_task:
        return jsonify({'error': 'Task already claimed'}), 403

    # Check if the task is already claimed by the user
    user_task = UserTask(user_id=user.id, cinema_task_id=task.id)
    session.add(user_task)
    session.commit()

    return jsonify({'message': 'Cinema task claimed successfully'}), 200

    user_id = request.json.get('user_id')
    user = session.query(User).filter_by(id=user_id).first()
    task = session.query(CinemaTask).filter_by(slug=slug).first()

    if not user or not task:
        return jsonify({'error': 'User or task not found'}), 404

    # Check if the user already claimed the task
    claimed_task = session.query(UserTask).filter_by(user_id=user.id, cinema_task_id=task.id).first()
    if claimed_task:
        return jsonify({'error': 'Task already claimed'}), 403

    # Mark the task as claimed
    user_task = UserTask(user_id=user.id, cinema_task_id=task.id)
    session.add(user_task)
    session.commit()

    return jsonify({'message': 'Cinema task claimed successfully'}), 200
@app.route('/api/channel-task/<int:id>/claim', methods=['POST'])
def claim_channel_task(id):
    task = session.query(ChannelTask).filter_by(id=id).first()
    if task:
        # فرض کنیم این متد کاربر فعلی را از request پیدا می‌کند
        user_id = request.json.get('user_id')

        if user_id:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                # به روز رسانی تسک
                task.user_id = user_id
                session.commit()
                return jsonify({'message': 'Channel task claimed successfully'}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'User ID is required'}), 400
    else:
        return jsonify({'error': 'Task not found'}), 404

    user_id = request.json.get('user_id')
    user = session.query(User).filter_by(id=user_id).first()
    task = session.query(ChannelTask).filter_by(id=id).first()

    if not user or not task:
        return jsonify({'error': 'User or task not found'}), 404

    # Check if the user already claimed the task
    claimed_task = session.query(UserTask).filter_by(user_id=user.id, channel_task_id=task.id).first()
    if claimed_task:
        return jsonify({'error': 'Task already claimed'}), 403

    # Mark the task as claimed
    user_task = UserTask(user_id=user.id, channel_task_id=task.id)
    session.add(user_task)
    session.commit()

    return jsonify({'message': 'Channel task claimed successfully'}), 200
@app.route('/api/referral-task/<int:id>/claim', methods=['POST'])
def claim_referral_task(id):
    task = session.query(ReferralTask).filter_by(id=id).first()
    if task:
        # فرض کنیم این متد کاربر فعلی را از request پیدا می‌کند
        user_id = request.json.get('user_id')  
        
        if user_id:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                # به روز رسانی تسک
                task.user_id = user_id
                session.commit()
                return jsonify({'message': 'Referral task claimed successfully'}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'User ID is required'}), 400
    else:
        return jsonify({'error': 'Task not found'}), 404
        

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
