from flask_caching import Cache
from flask import current_app as app
from application.database import db
from application.models import *

cache = Cache()


# @cache.memoize(timeout=300)
# def access_current_tracker(id):
#     cur_tracker = db.session.query(Tracker).filter(Tracker.id == id).first()
#     return cur_tracker


# @cache.memoize(timeout=300)
# def access_current_log(log_id):
#     logs = db.session.query(Log).filter(Log.log_id == log_id).first()
#     return logs


# @cache.memoize(timeout=300)
# def access_all_trackers(id):
#     trackers = db.session.query(Tracker).filter(Tracker.user_id == id).all()
#     return trackers


# @cache.memoize(timeout=300)
# def access_all_logs(id):
#     logs = db.session.query(Log).filter(Log.tracker_id == id).all()
#     return logs


# @cache.memoize(timeout=300)
# def access_all_users():
#     users = db.session.query(User).all()
#     return users

# @cache.memoize(timeout=300)
# def access_current_user(id):
#     user = db.session.query(User).filter(User.id == id).first()
#     return user