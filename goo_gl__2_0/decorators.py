from functools import wraps

from flask_login import current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from goo_gl__2_0.config import BaseConfig


def add_session_decorator(function_to_decorate):
    @wraps(function_to_decorate)
    def function_wrapper(*args, **kwargs):
        engine = create_engine(BaseConfig.DB_ADDRESS, echo=True)
        session = sessionmaker(bind=engine)()
        kwargs['session'] = session
        return_var = function_to_decorate(*args, **kwargs)
        session.close()
        return return_var
    return function_wrapper


def add_user_id(function_to_decorate):
    @wraps(function_to_decorate)
    def function_wrapper(*args, **kwargs):
        try:
            user_id = str(current_user.id)
        except (AttributeError, ValueError):
            user_id = '0'
        kwargs['current_user_id'] = user_id
        return_var = function_to_decorate(*args, **kwargs)
        return return_var
    return function_wrapper
