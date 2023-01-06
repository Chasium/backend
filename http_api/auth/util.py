from typing import Dict
from db import db
from db.models.user import UserData
from random import getrandbits
import re


login_user: Dict[str, int] = {}


def user_exists(username):
    user: UserData = UserData.query.filter_by(name=username).first()
    return True if user else False


def username_legal(username):
    username_rule = r'^[A-Za-z\d_]{3,32}$'
    matching = re.fullmatch(username_rule, username)
    return True if matching else False


def password_legal(password):
    p = r"^[A-Za-z\d~`!@#$%^&*()_\-+=\[\]\{\}|:;<>]{6,32}"
    matching = re.fullmatch(p, password)
    return True if matching else False


# user data interactions

def password_verified(username, password):
    user = UserData.query.filter_by(name=username).first()
    if user:
        return True if password == user.password else False
    else:
        return False


def add_user(username, password):
    # Add user to database
    new_user = UserData(username, password)
    db.session.add(new_user)
    db.session.commit()
    print('New user created')
    return


def get_session(user_id):  # not safe
    for session, user in login_user.items():
        if user == user_id:
            return session
    return hex(getrandbits(128))


# log in and out methods modifying session

def user_login(username):
    current_user: UserData = UserData.query.filter_by(name=username).first()
    if current_user:
        temp_session = get_session(current_user.id)
        login_user[temp_session] = current_user.id
        # print('user', username, 'login!')
        # print('session', temp_session)
    else:
        # raise error: undefined user
        print('undefined user')
        temp_session = None
    return temp_session


def logged_in(username):
    # Bug: user could be covered by other login users
    current_user: UserData = UserData.query.filter_by(name=username).first()
    if current_user:
        for user in login_user.values():
            if user == current_user.id:
                return True
    return False


def get_user(session: str) -> UserData:
    try:
        id = login_user[session]
        return UserData.query.filter_by(id=id).first()
    except KeyError:
        return None


def get_session_by_name(user_name: str) -> str:
    current_user: UserData = UserData.query.filter_by(
        name=user_name).first()
    if current_user:
        for session, user in login_user.items():
            if user == current_user.id:
                return session
    return None
