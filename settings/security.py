# This is for authentication and identity

from werkzeug.security import safe_str_cmp
from model.user import User

users = [
    User(1, 'Admin1', '@123'),
    User(2, 'Admin2', '@321'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    # check for user and return
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


# payload is the contents of the jwt token
def identity(payload):
    userid = payload['identity']
    return userid_table.get(userid, None)
