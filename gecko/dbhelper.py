import time

users = {'admin':
         {'uid': 1,
          'password': 'test3',
          'status': 'test',
          'expire_date': int(time.time() + 3600 * 24 * 7)}
         }


def get_user(username):
    return users.get(username, None)


def get_password(username):
    user = get_user(username)
    if user:
        return user['password']
    return None


def get_user_profile(username):
    user = get_user(username)
    if user:
        return dict(uid = user['uid'], username=username, status=user['status'], expire_date=user['expire_date'])
    return None
