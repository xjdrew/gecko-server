import time

users = {'admin':
         {'uid': 1,
          'password': 'test3',
          'status': 'test',
          'expire_date': int(time.time() + 3600 * 24 * 7)}
         }

servers = {
           1: dict(sid=1, user='test', password='youknonw', name="us-01", country="us", ip="www.baidu.com", noping = 0),
           2: dict(sid=2, user='test', password='youknonw', name="us-02", country="us", ip="www.yahoo.com", noping = 0),
           3: dict(sid=3, user='test', password='youknonw', name="us-03", country="us", ip="127.0.0.1", noping = 1),
           4: dict(sid=4, user='test', password='youknonw', name="us-04", country="us", ip="www.yahoo.com.jp", noping = 0),
           5: dict(sid=5, user='test', password='youknonw', name="us-05", country="us", ip="www.youku.com", noping = 0),
           6: dict(sid=6, user='test', password='youknonw', name="hk-01", country="hk", ip="183.128.67.96", noping = 0),
           7: dict(sid=7, user='test', password='youknonw', name="hk-02", country="hk", ip="www.hulu.com", noping = 0),
           8: dict(sid=8, user='test', password='youknonw', name="cn-01", country="cn", ip="121.12.13.23", noping = 0),
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

def get_server(sid):
    return servers.get(sid, None)

def get_server_profile(sid):
    server = get_server(sid)
    if server:
        return dict(sid=server['sid'], name=server['name'], country=server['country'], ip=server['ip'], noping=server['noping'])
    return None

def get_all_server_profile():
    keys = servers.keys()
    profiles = []
    for key in keys:
        profiles.append(get_server_profile(key))
    return profiles

def get_server_config(sid):
    server = get_server(sid)
    if server:
        return dict(sid=server['sid'], name=server['name'], ip=server['ip'], user=server['user'], password=server['password'])
    return None
