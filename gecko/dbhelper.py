import time

users = {'admin':
         {'uid': 1,
          'password': 'test3',
          'status': 'test',
          'expire_date': int(time.time() + 3600 * 24 * 7)}
         }

PROTOCAL_PPTP = 1
PROTOCAL_L2TP = 2

servers = {1: dict(sid=1, user='test', password='youknonw', name="us-01", country="us", ip="www.baidu.com", protocal=PROTOCAL_PPTP, noping=0),
           2: dict(sid=2, user='test', password='youknonw', name="us-02", country="us", ip="www.yahoo.com", protocal=PROTOCAL_PPTP, noping=0),
           3: dict(sid=3, user='test', password='youknonw', name="us-03", country="us", ip="127.0.0.1", protocal=PROTOCAL_PPTP, noping=1),
           4: dict(sid=4, user='test', password='youknonw', name="us-04", country="us", ip="www.yahoo.com.jp", protocal=PROTOCAL_PPTP, noping=0),
           5: dict(sid=5, user='test', password='youknonw', name="us-05-how-long-it-can-support", country="us", ip="www.youku.com", protocal=PROTOCAL_PPTP, noping=0),
           6: dict(sid=6, user='test', password='youknonw', name="hk-01", country="hk", ip="183.128.67.96", protocal=PROTOCAL_PPTP, noping=0),
           7: dict(sid=7, user='test', password='youknonw', name="hk-02", country="hk", ip="www.hulu.com", protocal=PROTOCAL_PPTP, noping=0),
           8: dict(sid=8, user='test', password='youknonw', name="cn-01", country="cn", ip="121.12.13.23", protocal=PROTOCAL_PPTP, noping=0),
           9: dict(sid=9, user='gecko-test', password='20130505', name='linode-test1', country="America", ip="96.126.96.243", protocal=PROTOCAL_PPTP | PROTOCAL_L2TP, token="mytoken", noping=0),
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
        return dict(uid=user['uid'], username=username, status=user['status'], expire_date=user['expire_date'])
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


class Server(dict):
    def is_pptp(self):
        return self['protocal'] & PROTOCAL_PPTP

    def is_l2tp(self):
        return self['protocal'] & PROTOCAL_L2TP


def get_server_config(sid):
    return Server(get_server(sid))
